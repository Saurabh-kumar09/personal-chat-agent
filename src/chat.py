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

1️⃣ **AI Chat** - Ask me anything! (Select Command: `/1`)
2️⃣ **Sheet-Thought** - Save your thoughts to sheet (Select Command: `/2`)
3️⃣ **To-Do** - Manage your to-do list (Select Command: `/3`)

Type the command to get started! 🚀""")


# Helper function to handle user messages and return the message text
async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_type: str = update.message.chat.type
    text: str = update.message.text

    user_message = update.message.text
    print(f'User ({update.message.chat.id}) in {chat_type}: "{text}"')
    return user_message


# Handler for ai chat with user - receives user message, gets ai response and sends it back to user
async def handle_ai_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = await handle_user_message(update, context)
    reply = ask_ai(user_message)

    await update.message.reply_text(reply)
    print(f'Bot: "{reply}"')


# Handler to save user message to sheet - receives user message, saves it to sheet and sends confirmation back to user
async def save_message_to_sheet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = await handle_user_message(update, context)
    save_text_to_sheet(user_message)

    await update.message.reply_text("Your message has been saved to the sheet!")
    print("Bot: Your message has been saved to the sheet!")


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

    else:
        await update.message.reply_text(
            "Invalid choice. Please type 1 for AI Chat, 2 for Sheet-Thought, or 3 for To-Do."
        )


# Handler to route messages based on user-selected mode - receives user message, checks mode in user_data and routes to appropriate handler
async def handle_mode_specific_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    mode = context.user_data.get("mode")

    if mode == "ai_chat":
        await handle_ai_chat(update, context)
    elif mode == "sheet_save":
        await save_message_to_sheet(update, context)
    elif mode == "to_do":
        # Here you would implement your to-do list handling logic
        await update.message.reply_text(
            "To-Do list functionality is not implemented yet."
        )
    else:
        await update.message.reply_text(
            "Select '/start' command to get started and for instructions on how to use the bot!"
        )


# Main function
def main():

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Register command handlers
    app.add_handler(CommandHandler("start", handle_start_command))

    # Handler for user choice of mode - only matches 1, 2, 3, /1, /2, /3 (FIRST - most specific)
    app.add_handler(
        MessageHandler(
            filters.TEXT & filters.Regex(r"^/?([123])$"),
            handle_user_command,
        )
    )

    # Listen to all other text messages and route based on mode (LAST - most general)
    app.add_handler(MessageHandler(filters.TEXT, handle_mode_specific_message))

    print("Bot is running...")

    app.run_polling()
