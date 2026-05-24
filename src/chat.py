from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

from src.ai_ask import ask_ai
from integrations.telegram_config import TELEGRAM_BOT_TOKEN
from src.store_text import save_text_to_sheet


# Command to start the bot
async def handle_start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""👋 Hey! How can I help you today?
        Choose a task to continue:
        1. 🤖 AI Chat
        2. 📄 Sheet-Thought
        3. ✅ To-Do
        Please type the number corresponding to your choice.""")


# Command to start ai chat
async def handle_chat_mode_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "You can start your chat with ai - just type your message!"
    )


# Command to save text in sheet
async def handle_sheet_save_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "You can save text in the sheet - just type your message!"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_type: str = update.message.chat.type
    text: str = update.message.text

    user_message = update.message.text
    print(f'User ({update.message.chat.id}) in {chat_type}: "{text}"')
    reply = ask_ai(user_message)

    await update.message.reply_text(reply)
    print(f'Bot: "{reply}"')


async def save_message_to_sheet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_type: str = update.message.chat.type
    text: str = update.message.text

    user_message = update.message.text
    print(f'User ({update.message.chat.id}) in {chat_type}: "{text}"')
    save_text_to_sheet(user_message)

    await update.message.reply_text("Your message has been saved to the sheet!")
    print("Bot: Your message has been saved to the sheet!")


# Main function
def main():

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Register command handlers
    app.add_handler(CommandHandler("start", handle_start_command))
    app.add_handler(CommandHandler("1", handle_chat_mode_command))
    app.add_handler(CommandHandler("2", handle_sheet_save_command))

    # Listen to all text messages
    app.add_handler(MessageHandler(filters.TEXT, save_message_to_sheet))

    print("Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
