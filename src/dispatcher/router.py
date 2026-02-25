from dataclasses import dataclass
import re
from typing import Dict
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters
# from src.handlers.sheet_manager import handle_sheet_command
from src.handlers.expense_handler import handle_expense_command
from src.utils.logger import logger

@dataclass
class DispatchResult:
    """Represents the result of routing a message."""
    handler_name: str
    payload: Dict

class CommandRouter:
    """Routes incoming raw messages to the appropriate handler."""

    SYSTEM_COMMANDS = {"format","formate",'link'}
    # SYSTEM_COMMANDS = {"ls", "mk", "select", "current", "del", "--help", "format"}

    def route(self, message: str) -> DispatchResult:
        message = self._normalize_message(message)
        # if not message:
        #     return self._unknown_command_response()

        if self._is_system_command(message):
            payload = self._extract_system_command(message)
            return DispatchResult(handler_name="sheet_manager", payload=payload)

        if self._is_expense_command(message):
            payload = {"raw_expense": message}
            return DispatchResult(handler_name="expense_handler", payload=payload)

        return self._unknown_command_response()

    def _normalize_message(self, message: str) -> str:
        if not isinstance(message, str): return ""
        return re.sub(r"\s+", " ", message.strip())

    def _is_system_command(self, message: str) -> bool:
        lower_msg = message.lower()
        return any(lower_msg == cmd or lower_msg.startswith(f"{cmd} ") for cmd in self.SYSTEM_COMMANDS)

    def _is_expense_command(self, message: str) -> bool:
        return bool(re.match(r"^\d+", message))

    def _extract_system_command(self, message: str) -> Dict:
        parts = message.split(" ", 1)
        return {"command": parts[0].lower(), "args": parts[1].strip() if len(parts) > 1 else ""}

    def _unknown_command_response(self) -> DispatchResult:
        return DispatchResult(handler_name="error", payload={"message": "❌ Unknown command."})

# router = CommandRouter()


# async def dispatch_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Orchestrates routing and handler execution."""
#     text = update.message.text
#     result = router.route(text)
    
#     logger.info(f"Routing message: '{text}' -> {result.handler_name}")
    
#     if result.handler_name == "sheet_manager":
#         await handle_sheet_command(update, context, result.payload)
#     elif result.handler_name == "expense_handler":
#         await handle_expense_command(update, context, result.payload)
#     else:
#         await update.message.reply_text(result.payload.get("message", "Error"))

# def setup_router(application):
#     """Registers handlers with the Telegram application."""
#     application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, dispatch_message))
#     # Add explicit command handlers if needed, or route all through dispatch_message
#     application.add_handler(CommandHandler(list(CommandRouter.SYSTEM_COMMANDS), dispatch_message))
