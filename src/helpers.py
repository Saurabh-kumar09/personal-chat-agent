# Decorator factory for handlers that save content to sheets
from functools import wraps

from telegram import Update
from telegram.ext import (
    ContextTypes,
)
from bs4 import BeautifulSoup
import requests

from src.chat_engine import generate_chat_response

"""
This module contains helper functions for the Telegram bot, including:
- A decorator factory for handlers that save content to Google Sheets   
- A helper function to extract user messages from updates
- Functions to extract text from URLs and summarize content using the chat engine.
"""


# save to sheet decorator factory - takes in the function to save to sheet and the success message to send back to user,
# returns a decorator that wraps the handler function.
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


# Helper function to handle user messages and return the message text
async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_type: str = update.message.chat.type
    text: str = update.message.text

    user_message = update.message.text
    print(f'User ({update.message.chat.id}) in {chat_type}: "{text}"')
    return user_message


# Function to extract text content from a URL using requests and BeautifulSoup
def extract_text_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove unwanted tags
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()

        text = soup.get_text(separator=" ")

        # Clean extra spaces
        text = " ".join(text.split())

        return text

    except requests.exceptions.Timeout:
        print("Failed to fetch URL: Request timed out.")
        return None

    except requests.exceptions.RequestException as error:
        print(f"Failed to fetch URL: {error}")
        return None


# Function to summarize content from a URL using the generate_chat_response function with a structured prompt
def summarize_url(url, word_limit=100):
    article_text = extract_text_from_url(url)

    if not article_text:
        return {
            "summary": "Unable to fetch content from the provided URL.",
            "keyword": "",
        }

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
