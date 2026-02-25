from datetime import datetime
from src.utils.logger import logger
# from src.api.sheets_api import SheetsAP
import gspread
from google.oauth2.service_account import Credentials

# SINGLE SHEET CONFIG (one-time)
SHEET_NAME = "Track Expenses"   # only for user messages
# sheets_api should be created ONCE (e.g. in main.py) and injected
# Example:
# sheets_api = SheetsAPI(sheet_id="1AbCdEf...")

def handle_expense_command(payload: dict) -> str:
    """
    Handle expense entry.
    Parses the raw expense and appends it to ONE Google Sheet.

    Expected format:
    <amount>, <description>, <category> [, mode] [, notes]
    """

    raw_expense = payload.get("raw_expense")
    
    SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_file(
        "credentials/service_account.json",
        scopes=SCOPES
    )

    client = gspread.authorize(creds)
    sheets_api = client.open("Track Expenses").sheet1

    logger.info(f"[ExpenseHandler] Raw expense received: {raw_expense}")

    if not raw_expense or not isinstance(raw_expense, str):
        return "❌ Invalid expense input."

    # ---------------------------------
    # 1. Normalize & split input
    # ---------------------------------
    parts = [p.strip() for p in raw_expense.split(",") if p.strip()]

    if len(parts) < 3:
        return (
            "❌ Invalid expense format.\n"
            "Use:\n"
            "<amount>, <description>, <category>, <mode>, <notes>"
        )

    # ---------------------------------
    # 2. Extract fields with defaults
    # ---------------------------------
    print(parts)
    amount_raw = parts[0]
    description = parts[1]
    category = parts[2]

    mode = parts[3] if len(parts) >= 4 else "cash"
    notes = parts[4] if len(parts) >= 5 else ""

    # ---------------------------------
    # 3. Validate & normalize
    # ---------------------------------
    try:
        amount = float(amount_raw)
    except ValueError:
        return "❌ Amount must be a valid number."

    description = description.strip()
    category = category.strip().lower()
    mode = mode.strip().lower()
    notes = notes.strip()

    # ---------------------------------
    # 4. Auto add date & time (12-hour)
    # ---------------------------------
    now = datetime.now()

    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%I:%M:%S %p")   # 12-hour format

    # ---------------------------------
    # 5. Prepare row (sheet-ready)
    # ---------------------------------
    row = [
        date_str,      # Date
        time_str,      # Time (12-hr)
        description,   # Description
        amount,        # Amount
        mode,          # Payment Mode
        category,      # Category
        notes,         # Notes (optional)
        "telegram",    # Source
    ]

    logger.info(f"[ExpenseHandler] Appending row: {row}")

    # ---------------------------------
    # 6. Append row to CLOUD sheet
    # ---------------------------------
    try:
        sheets_api.append_row(row)
    except Exception:
        logger.exception("[ExpenseHandler] Failed to append expense")
        return "❌ Failed to save expense. Please try again."

    # ---------------------------------
    # 7. User response
    # ---------------------------------
    response = (
        f"✅ Expense added\n"
        f"• {description}\n"
        f"• ₹{amount} via {mode}\n"
        f"• Category: {category}"
    )

    if notes:
        response += f"\n• Notes: {notes}"

    return response
