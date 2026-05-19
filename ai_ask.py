import config as cfg
import prompt as instruction


def ask_ai(user_message):
    system_instruction = instruction.instruction_prompt(user_message)

    response = cfg.client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=system_instruction,
    )

    reply = response.text
    return reply
