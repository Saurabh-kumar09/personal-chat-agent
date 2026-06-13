"""Google Sheets API Configuration"""

import json
import os
from pathlib import Path
from dotenv import load_dotenv
import gspread
from google.oauth2.service_account import Credentials

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Google sheet api authentication and setup
SCOPES = [
    os.getenv("GOOGLE_SHEETS_SCOPE", "https://www.googleapis.com/auth/spreadsheets")
]

google_credentials_json = os.getenv("GOOGLE_CREDENTIALS_JSON")

if not google_credentials_json:
    raise ValueError(
        "GOOGLE_CREDENTIALS_JSON not found in environment variables. "
        "Set it to the service account JSON or to a file path like credentials.json."
    )


# Helper functions to load credentials from JSON or file path
def _credential_paths(credentials_value):
    credentials_path = Path(credentials_value).expanduser()

    if credentials_path.is_absolute():
        return [credentials_path]

    return [
        Path.cwd() / credentials_path,
        PROJECT_ROOT / credentials_path,
    ]


# Load credentials from JSON string or file path
def _load_credentials_info(credentials_value):
    credentials_value = credentials_value.strip()

    if credentials_value.startswith("{"):
        try:
            return json.loads(credentials_value)
        except json.JSONDecodeError as error:
            raise ValueError("GOOGLE_CREDENTIALS_JSON contains invalid JSON") from error

    credential_paths = _credential_paths(credentials_value)

    for credential_path in credential_paths:
        try:
            if credential_path.is_file():
                with credential_path.open("r", encoding="utf-8") as credentials_file:
                    try:
                        return json.load(credentials_file)
                    except json.JSONDecodeError as error:
                        raise ValueError(
                            f"Google credentials file is not valid JSON: {credential_path}"
                        ) from error
        except OSError:
            continue

    try:
        return json.loads(credentials_value)
    except json.JSONDecodeError as error:
        checked_paths = ", ".join(str(path) for path in credential_paths)
        raise ValueError(
            "GOOGLE_CREDENTIALS_JSON must be service account JSON or a path to a "
            f"service account JSON file. Checked paths: {checked_paths}"
        ) from error


credentials_info = _load_credentials_info(google_credentials_json)

credentials = Credentials.from_service_account_info(
    credentials_info,
    scopes=SCOPES,
)
sheets_client = gspread.authorize(credentials)

GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
if not GOOGLE_SHEET_ID:
    raise ValueError("GOOGLE_SHEET_ID not found in environment variables")

try:
    sheet = sheets_client.open_by_key(GOOGLE_SHEET_ID)
except gspread.exceptions.SpreadsheetNotFound as error:
    raise ValueError(
        "Google Sheet not found. Check GOOGLE_SHEET_ID and make sure the sheet "
        "is shared with the service account email from your credentials."
    ) from error
except Exception as error:
    raise RuntimeError(
        "Failed to connect to Google Sheets. Check your internet connection, "
        "GOOGLE_SHEET_ID, service account credentials, and sheet sharing."
    ) from error

print("Connected successfully!")
