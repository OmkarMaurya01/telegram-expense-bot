import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE", "credentials/service_account.json")

# State file paths
SHEETS_REGISTRY = "src/state/sheets.json"
ACTIVE_SHEET_FILE = "src/state/active_sheet.json"
