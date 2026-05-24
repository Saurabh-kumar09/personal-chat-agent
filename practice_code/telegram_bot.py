from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    filters,
    ContextTypes,
)

from integrations.telegram_config import TELEGRAM_BOT_TOKEN


# Function to reply to messages
async def reply_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_text = update.message.text.lower()

    if user_text == "hi":
        await update.message.reply_text("Hello from Python Bot 🚀")

    else:
        await update.message.reply_text(f"You said: {user_text}")


# Main function
def main():

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Listen to all text messages
    app.add_handler(MessageHandler(filters.TEXT, reply_message))

    print("Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
