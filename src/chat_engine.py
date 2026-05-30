from integrations.gemini_config import client
import prompts.system_prompt as instruction

conversation = []


def generate_chat_response(user_message):

    # store current user message
    conversation.append(f"User: {user_message}")

    # keep short-term memory small
    recent_conversation = "\n".join(conversation[-6:])

    # build strong dynamic prompt
    final_prompt = f"""
    {instruction.instruction_prompt(user_message)}

    Previous Conversation Context:
    {recent_conversation}

    Current User Message:
    {user_message}

    Generate response according to all system rules above.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=final_prompt,
    )

    reply = response.text

    # store assistant response
    conversation.append(f"Assistant: {reply}")

    return reply
