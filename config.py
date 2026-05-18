"""Configurations for the Google Sheets API and Gemini API"""

import os
from google import genai
from dotenv import load_dotenv
import gspread
from google.oauth2.service_account import Credentials

load_dotenv()

# llm - Google Gemini API key setup and client initialization
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)
print("Gemini API client initialized successfully!")

# Google sheet api authentication and setup
SCOPES = [
    os.getenv("GOOGLE_SHEETS_SCOPE", "https://www.googleapis.com/auth/spreadsheets")
]
CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials.json")

creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
clientSheet = gspread.authorize(
    creds
)  # authorizes the client with the provided credentials

# open sheet by key from environment variable
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
sheet = clientSheet.open_by_key(GOOGLE_SHEET_ID)
print("Connected successfully!")
