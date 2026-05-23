"""Gemini AI Configuration"""

import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Google Gemini API key setup and client initialization
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)
print("Gemini API client initialized successfully!")
