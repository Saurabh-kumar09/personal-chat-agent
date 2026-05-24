from integrations.gemini_config import client
import prompts.system_prompt as instruction


def ask_ai(user_message):
    system_instruction = instruction.instruction_prompt(user_message)

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=system_instruction,
    )

    reply = response.text
    return reply
