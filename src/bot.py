from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

from src.chat_engine import generate_chat_response
from integrations.telegram_config import TELEGRAM_BOT_TOKEN
from src.save_to_sheet import (
    add_thoughts_to_sheet,
    add_todo_to_sheet,
    add_url_to_sheet,
)
from functools import wraps
import requests
from bs4 import BeautifulSoup


# Decorator factory for handlers that save content to sheets
def save_to_sheet(save_function, success_message):
    """
    Decorator factory that wraps handlers to save content to sheets.

    Args:
        save_function: Function to call for saving (e.g., add_thoughts_to_sheet, add_todo_to_sheet)
        success_message: Message to send back to user after successful save

    Returns:
        A decorator that wraps async handler functions
    """

    def decorator(handler_func):
        @wraps(handler_func)
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
            # Get user message
            user_message = await handle_user_message(update, context)
            # Save to sheet using provided function
            save_function(user_message)
            # Send confirmation to user
            await update.message.reply_text(success_message)
            print(f"Bot: {success_message}")

        return wrapper

    return decorator


"Utility functions"


# Helper function to handle user messages and return the message text
async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_type: str = update.message.chat.type
    text: str = update.message.text

    user_message = update.message.text
    print(f'User ({update.message.chat.id}) in {chat_type}: "{text}"')
    return user_message


# Function to extract text content from a URL using requests and BeautifulSoup
def extract_text_from_url(url):
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove unwanted tags
    for tag in soup(["script", "style", "nav", "footer"]):
        tag.decompose()

    text = soup.get_text(separator=" ")

    # Clean extra spaces
    text = " ".join(text.split())

    return text


# Function to summarize content from a URL using the generate_chat_response function with a structured prompt
def summarize_url(url, word_limit=100):
    article_text = extract_text_from_url(url)
    keyword = ""

    prompt = f"""
    Analyze the following webpage content and extract:
    1. one strong categorization keyword
    2. the main topic
    3. a concise 5-point summary
    
    TASK:
    - Understand the core subject of the webpage
    - Identify the most meaningful keyword for categorization
    - Summarize the content clearly and concisely
    
    OUTPUT FORMAT:
    KEYWORD: <single categorization keyword>
    
    TOPIC:
    <one-line topic summary>
    
    SUMMARY:
    1. ...
    2. ...
    3. ...
    4. ...
    5. ...
    
    KEYWORD RULES:
    - Return ONLY one keyword
    - The keyword should represent the main category or domain of the content
    - Prefer specific and meaningful keywords over generic ones
    - Avoid overly broad keywords like:
      - Technology
      - AI
      - News
      - Business
    - Prefer keywords useful for tagging, grouping, or organizing content
    - Do not repeat the keyword inside summary points
    - Keep keyword short and clean
    
    SUMMARY RULES:
    - Keep the full response within {word_limit} words
    - Keep points short, informative, and readable
    - Avoid repetition
    - Avoid filler language
    - Focus on the most useful information only
    - Do not include conclusion or closing remarks
    - Use clear and natural language
    - Follow instruction_prompt response style naturally

    IMPORTANT:
    - Prioritize clarity and usefulness
    - Maintain clean formatting
    - Avoid markdown-heavy formatting
    - Keep the response easy to scan

    WEBPAGE CONTENT:
    {article_text[:15000]}
    """

    result = generate_chat_response(prompt)

    lines = result.splitlines()

    keyword = ""
    cleaned_response = []

    for line in lines:

        if line.startswith("KEYWORD:"):
            keyword = line.replace("KEYWORD:", "").strip()

        else:
            cleaned_response.append(line)

    summary = "\n".join(cleaned_response).strip()

    return {
        "summary": summary,
        "keyword": keyword,
    }


"Feature Handlers"


# Handler for ai chat with user - receives user message, gets ai response and sends it back to user
async def handle_ai_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = await handle_user_message(update, context)
    reply = generate_chat_response(user_message)

    await update.message.reply_text(reply)
    print(f'Bot: "{reply}"')


# Handlers for saving thoughts and todos to sheets
@save_to_sheet(add_thoughts_to_sheet, "Thought saved!")
def save_thought(update, context):
    pass


@save_to_sheet(add_todo_to_sheet, "Todo saved!")
def save_todo(update, context):
    pass


# Handler for summarizing content from a URL
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
    add_url_to_sheet(user_message, keyword)
    await update.message.reply_text(summary)
    print(f'Bot: "{summary}"')


"Routing Handlers"


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
