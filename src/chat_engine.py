import logging
import time

from integrations.gemini_config import client
import prompts.system_prompt as instruction


conversation = []

MAX_RETRIES = 3


def generate_chat_response(user_message):

    try:
        # Store current user message
        conversation.append(f"User: {user_message}")

        # Keep short-term memory small
        recent_conversation = "\n".join(conversation[-6:])

        # Build dynamic prompt
        final_prompt = build_prompt(
            user_message=user_message,
            recent_conversation=recent_conversation,
        )

        # Generate AI response safely
        reply = fetch_gemini_response(final_prompt)

        # If AI failed gracefully
        if not reply:
            return "AI service is temporarily unavailable."

        # Store assistant response
        conversation.append(f"Assistant: {reply}")

        return reply

    except Exception:
        logging.exception("Unexpected error in generate_chat_response")

        return "Something went wrong while generating response."


def build_prompt(user_message, recent_conversation):

    return f"""
    {instruction.instruction_prompt(user_message)}

    Previous Conversation Context:
    {recent_conversation}

    Current User Message:
    {user_message}

    Generate response according to all system rules above.
    """

def fetch_gemini_response(prompt):

    delay = 1

    for attempt in range(MAX_RETRIES):

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )

            # Validate response
            if not response:
                logging.error("Empty Gemini response")
                return None

            if not hasattr(response, "text"):
                logging.error("Missing response.text")
                return None

            if not response.text:
                logging.error("Empty response text")
                return None

            return response.text.strip()

        except Exception as e:

            error_message = str(e)

            logging.error(
                f"Gemini API failed on attempt {attempt + 1}: {error_message}"
            )

            # ===== NON-RETRYABLE ERRORS =====

            if "RESOURCE_EXHAUSTED" in error_message:
                logging.error("Gemini credits/quota exhausted")
                return (
                    "AI quota exhausted. Please try again later."
                )

            if "API_KEY_INVALID" in error_message:
                logging.error("Invalid Gemini API key")
                return (
                    "AI configuration error."
                )

            # ===== RETRYABLE ERRORS =====

            if attempt < MAX_RETRIES - 1:
                time.sleep(delay)
                delay *= 2

    return "AI service temporarily unavailable."