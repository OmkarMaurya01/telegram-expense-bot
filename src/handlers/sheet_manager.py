from telegram import Update
from telegram.ext import ContextTypes
from src.utils.logger import logger

import json
import os
import logging
# from src.api.drive_api import DriveAPI

logger = logging.getLogger(__name__)

SHEETS_PATH = "state/sheets.json"
ACTIVE_SHEET_PATH = "state/active_sheet.json"


def _load_sheets():
    if not os.path.exists(SHEETS_PATH):
        return {"sheets": []}
    with open(SHEETS_PATH, "r") as f:
        return json.load(f)


def _save_sheets(data):
    os.makedirs(os.path.dirname(SHEETS_PATH), exist_ok=True)
    with open(SHEETS_PATH, "w") as f:
        json.dump(data, f, indent=2)


def _set_active_sheet(sheet):
    with open(ACTIVE_SHEET_PATH, "w") as f:
        json.dump(sheet, f, indent=2)


def _get_active_sheet():
    if not os.path.exists(ACTIVE_SHEET_PATH):
        return None
    with open(ACTIVE_SHEET_PATH, "r") as f:
        return json.load(f)


def handle_sheet_command(payload: dict) -> str:
    """
    Handle system-level sheet commands.
    """

    command = payload.get("command")
    args = payload.get("args", "").strip()

    logger.info(f"[SheetManager] Command={command}, Args={args}")
    
    if command == 'formate' or command == 'format':
        return "<amount>, <description>, <category>, <mode>, <notes>"
    
    if command == "link":
        return 'https://docs.google.com/spreadsheets/d/1wZyHKp4rZ0ysFN8S4DjflLpIy0g_lPsrWhsEBg1nFsY/edit?gid=0#gid=0'

  
        

    # drive_api = DriveAPI()
    # data = _load_sheets()
    # sheets = data["sheets"]

    # -------------------------
    # ls
    # -------------------------
    # if command == "ls":
    #     if not sheets:
    #         return "📄 No sheets available."

    #     response = ["📄 Available sheets:"]
    #     for idx, s in enumerate(sheets, start=1):
    #         response.append(f"{idx}. {s['sheet_name']}")

    #     return "\n".join(response)

    # -------------------------
    # mk sheet <name>
    # -------------------------
    # elif command == "mk":
    #     if not args.lower().startswith("sheet "):
    #         return "❌ Usage: mk sheet <sheet_name>"

    #     sheet_name = args[6:].strip()

    #     if not sheet_name:
    #         return "❌ Sheet name cannot be empty."

    #     result = drive_api.create_spreadsheet(sheet_name)

    #     sheet_entry = {
    #         "sheet_id": result["sheet_id"],
    #         "sheet_name": result["sheet_name"]
    #     }

    #     sheets.append(sheet_entry)
    #     _save_sheets(data)
    #     _set_active_sheet(sheet_entry)

    #     return f"✅ Sheet created & selected: *{sheet_name}*"

    # -------------------------
    # select <index | name>
    # -------------------------
    # elif command == "select":
    #     if not args:
    #         return "❌ Usage: select <index | sheet_name>"

    #     selected = None

    #     if args.isdigit():
    #         idx = int(args) - 1
    #         if idx < 0 or idx >= len(sheets):
    #             return "❌ Invalid sheet index."
    #         selected = sheets[idx]
    #     else:
    #         for s in sheets:
    #             if s["sheet_name"].lower() == args.lower():
    #                 selected = s
    #                 break

    #     if not selected:
    #         return "❌ Sheet not found."

    #     _set_active_sheet(selected)
    #     return f"📌 Active sheet set to: *{selected['sheet_name']}*"

    # -------------------------
    # current
    # -------------------------
    # elif command == "current":
    #     active = _get_active_sheet()
    #     if not active:
    #         return "📍 No active sheet selected."
    #     return f"📍 Current sheet: *{active['sheet_name']}*"

    # -------------------------
    # del <index | name>
    # -------------------------
    # elif command == "del":
    #     if not args:
    #         return "❌ Usage: del <index | sheet_name>"

    #     target = None

    #     if args.isdigit():
    #         idx = int(args) - 1
    #         if idx < 0 or idx >= len(sheets):
    #             return "❌ Invalid sheet index."
    #         target = sheets[idx]
    #     else:
    #         for s in sheets:
    #             if s["sheet_name"].lower() == args.lower():
    #                 target = s
    #                 break

    #     if not target:
    #         return "❌ Sheet not found."

    #     success = drive_api.delete_spreadsheet(target["sheet_id"])
    #     if not success:
    #         return "❌ Failed to delete sheet."

    #     sheets.remove(target)
    #     _save_sheets(data)

    #     active = _get_active_sheet()
    #     if active and active["sheet_id"] == target["sheet_id"]:
    #         os.remove(ACTIVE_SHEET_PATH)

    #     return f"🗑️ Sheet deleted: *{target['sheet_name']}*"

    # -------------------------
    # fallback
    # -------------------------
    # else:
        # return f"❌ Unknown system command: {command}"
