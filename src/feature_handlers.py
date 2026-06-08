from telegram import Update
from telegram.ext import (
    ContextTypes,
)
from src.helpers import handle_user_message, summarize_url, save_to_sheet
from src.chat_engine import generate_chat_response
from src.save_to_sheet import add_thoughts_to_sheet, add_todo_to_sheet, add_url_to_sheet

"""
This module contains the Telegram bot handlers for different user interactions, including:
- AI chat responses
- Saving thoughts and todos to Google Sheets
- Summarizing content from URLs and saving them to sheets
"""


# Handler for ai chat with user - receives user message, gets ai response and sends it back to user
async def handle_ai_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = await handle_user_message(update, context)
    reply = generate_chat_response(user_message)

    await update.message.reply_text(reply)
    print(f'Bot: "{reply}"')


# Handler for saving thoughts to sheet
@save_to_sheet(add_thoughts_to_sheet, "Thought saved!")
def save_thought(update, context):
    pass


# Handler for saving todos to sheet
@save_to_sheet(add_todo_to_sheet, "Todo saved!")
def save_todo(update, context):
    pass


async def handle_summarize_url(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_message = await handle_user_message(update, context)

    if not user_message.startswith("http"):
        await update.message.reply_text(
            "Please send a valid URL starting with http or https."
        )
        return

    result = summarize_url(user_message)

    summary = result["summary"]
    keyword = result["keyword"]

    print(f"Extracted keyword: {keyword}")

    url_saved = add_url_to_sheet(user_message, keyword)

    if not url_saved:
        return False

    await update.message.reply_text(summary)

    print(f'Bot: "{summary}"')
