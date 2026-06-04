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


# Handler to process user command for mode selection - receives user message, sets mode in user_data and sends confirmation back to user
async def handle_user_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = await handle_user_message(update, context)

    # Strip whitespace AND remove leading '/' if present
    user_choice = user_message.strip().lstrip("/")

    if user_choice == "1":
        context.user_data["mode"] = "ai_chat"
        await update.message.reply_text(
            "You can start your chat with ai - just type your message!"
        )

    elif user_choice == "2":
        context.user_data["mode"] = "sheet_save"
        await update.message.reply_text(
            "You can save text in the sheet - just type your message!"
        )

    elif user_choice == "3":
        context.user_data["mode"] = "to_do"
        await update.message.reply_text(
            "You can manage your to-do list - just type your message!"
        )

    elif user_choice == "4":
        context.user_data["mode"] = "summarize_url"
        await update.message.reply_text(
            "You can summarize content from a URL - just send the URL!"
        )

    else:
        await update.message.reply_text(
            "Invalid choice. Please select a valid option by command: /1, /2, /3 or /4"
        )


# Handler to route messages based on user-selected mode - receives user message,
# checks mode in user_data and routes to appropriate handler
async def handle_mode_specific_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
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


# startup handler
async def handle_start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""👋 Hey! How can I help you today?

Choose a task to continue:

1️⃣ **AI Chat** - Ask me anything! (Select Command: `/1`)
2️⃣ **Sheet-Thought** - Save your thoughts to sheet (Select Command: `/2`)
3️⃣ **To-Do** - Manage your to-do list (Select Command: `/3`)
4️⃣ **Summarize URL** - Get a summary of a webpage (Select Command: `/4`)

Type the command to get started! 🚀""")


# Main function to set up the bot, register handlers and start polling for updates
def main():

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Register command handlers
    app.add_handler(CommandHandler("start", handle_start_command))

    # Handler for user choice of mode - only matches 1, 2, 3, /1, /2, /3 (FIRST - most specific)
    app.add_handler(
        MessageHandler(
            filters.TEXT & filters.Regex(r"^/?([1234])$"),
            handle_user_command,
        )
    )

    # Listen to all other text messages and route based on mode (LAST - most general)
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_mode_specific_message)
    )

    print("Bot is running...")

    app.run_polling()
