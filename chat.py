import os

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    filters,
    ContextTypes,
)

from ai_ask import ask_ai
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_type: str = update.message.chat.type
    text: str = update.message.text

    user_message = update.message.text
    print(f'User ({update.message.chat.id}) in {chat_type}: "{text}"')
    reply = ask_ai(user_message)

    await update.message.reply_text(reply)
    print(f'Bot: "{reply}"')


# Main function
def main():

    app = ApplicationBuilder().token(TOKEN).build()

    # Listen to all text messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    print("Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
