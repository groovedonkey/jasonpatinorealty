import os
import json
import logging
from typing import Optional
import gspread
from google.oauth2.service_account import Credentials

logger = logging.getLogger(__name__)

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

SPREADSHEET_ID = os.getenv("GOOGLE_SPREADSHEET_ID", "")
GOOGLE_CREDENTIALS_JSON = os.getenv("GOOGLE_CREDENTIALS_JSON", "")


def _get_client() -> Optional[gspread.Client]:
    """Authenticate and return a gspread client, or None if not configured."""
    if not GOOGLE_CREDENTIALS_JSON or not SPREADSHEET_ID:
        logger.warning("Google Sheets not configured — skipping.")
        return None

    try:
        creds_dict = json.loads(GOOGLE_CREDENTIALS_JSON)
        creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
        return gspread.authorize(creds)
    except Exception as e:
        logger.error(f"Failed to authenticate with Google Sheets: {e}")
        return None


def append_contact_to_sheet(
    first_name: str, last_name: str, business_name: str,
    phone: str, email: str, interest: str, message: str, created_at: str,
):
    """Append a new contact row to the configured Google Sheet."""
    client = _get_client()
    if client is None:
        return

    try:
        sheet = client.open_by_key(SPREADSHEET_ID).sheet1
        sheet.append_row(
            [first_name, last_name, business_name, phone, email, interest, message, created_at],
            value_input_option="USER_ENTERED",
        )
        logger.info(f"Appended contact '{first_name} {last_name}' to Google Sheet.")
    except Exception as e:
        logger.error(f"Failed to append to Google Sheet: {e}")
