from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

from integrations.telegram_config import TELEGRAM_BOT_TOKEN

from src.feature_handlers import (
    handle_ai_chat,
    handle_summarize_url,
    save_thought,
    save_todo,
)

from src.helpers import handle_user_message

"""
This module contains the main Telegram bot setup, including:
- Command handlers for user interactions
- Routing messages based on user-selected mode
- Startup handler to welcome users and provide instructions
"""


# Mode configuration
MODE_CONFIG = {
    "1": (
        "ai_chat",
        "You can start your chat with ai - just type your message!",
    ),
    "2": (
        "sheet_save",
        "You can save text in the sheet - just type your message!",
    ),
    "3": (
        "to_do",
        "You can manage your to-do list - just type your message!",
    ),
    "4": (
        "summarize_url",
        "You can summarize content from a URL - just send the URL!",
    ),
}


# Startup handler
async def handle_start_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    await update.message.reply_text("""👋 Hey! How can I help you today?

Choose a task to continue:

1️⃣ **AI Chat** - Ask me anything! (Select Command: `/1`)
2️⃣ **Sheet-Thought** - Save your thoughts to sheet (Select Command: `/2`)
3️⃣ **To-Do** - Manage your to-do list (Select Command: `/3`)
4️⃣ **Summarize URL** - Get a summary of a webpage (Select Command: `/4`)

Type the command to get started! 🚀""")


# Handler to process mode selection
async def handle_mode_selection(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    user_message = await handle_user_message(update, context)

    user_choice = user_message.strip().lstrip("/")

    selected_mode = MODE_CONFIG.get(user_choice)

    if not selected_mode:
        await update.message.reply_text(
            "Invalid choice. Please select a valid option by command: /1, /2, /3 or /4"
        )
        return

    mode, confirmation_message = selected_mode

    context.user_data["mode"] = mode

    await update.message.reply_text(confirmation_message)


# Handler to route messages based on user-selected mode
async def handle_mode_specific_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    mode = context.user_data.get("mode")

    if mode == "ai_chat":
        await handle_ai_chat(update, context)

    elif mode == "sheet_save":
        await save_thought(update, context)

    elif mode == "to_do":
        await save_todo(update, context)

    elif mode == "summarize_url":
        await handle_summarize_url(update, context)

    else:
        await update.message.reply_text(
            "Select '/start' command to get started and for instructions on how to use the bot!"
        )


# Main function to set up the bot, register handlers and start polling
def main():

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Register command handlers
    app.add_handler(CommandHandler("start", handle_start_command))

    # Handler for mode selection
    app.add_handler(
        MessageHandler(
            filters.TEXT & filters.Regex(r"^/?([1234])$"),
            handle_mode_selection,
        )
    )

    # Route all other text messages based on selected mode
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_mode_specific_message,
        )
    )

    print("Bot is running...")

    app.run_polling()
