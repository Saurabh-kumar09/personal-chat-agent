"""Google Sheets API Configuration"""

import os
from dotenv import load_dotenv
import gspread
from google.oauth2.service_account import Credentials

load_dotenv()

# Google sheet api authentication and setup
SCOPES = [
    os.getenv("GOOGLE_SHEETS_SCOPE", "https://www.googleapis.com/auth/spreadsheets")
]
CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials.json")

credentials = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
sheets_client = gspread.authorize(
    credentials
)  # authorizes the client with the provided credentials

# open sheet by key from environment variable
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
sheet = sheets_client.open_by_key(GOOGLE_SHEET_ID)
print("Connected successfully!")
