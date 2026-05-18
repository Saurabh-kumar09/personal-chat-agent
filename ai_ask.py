import config as cfg


def ask_ai(user_message):
    conversation = [user_message]

    response = cfg.client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=conversation,
    )

    reply = response.text
    return reply
