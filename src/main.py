# from src.bot.telegram_bot import run_bot
# from src.utils.logger import logger

from src.bot import telegram_bot
from src.dispatcher import router 
from src.handlers import expense_handler
from src.utils import logger
from src.handlers import sheet_manager
from src.utils.keep_alive import keep_alive
def process_message(message: str) -> str:
    """
    This is your central processing function.

    Telegram → this function → response
    """
    print("[Main] Processing message:", message)
    router_obj = router.CommandRouter()
    result = router_obj.route(message=message)

    message = '❌   Invalid Argument'
    
    if result.handler_name == "sheet_manager":
        message = sheet_manager.handle_sheet_command(result.payload)
    
    if result.handler_name == "expense_handler":
        message = expense_handler.handle_expense_command(result.payload)

    return message 


def main():
    print("[Main] Starting application...")

    # Start Telegram bot and pass processing function
    telegram_bot.start_telegram_bot(process_message)




if __name__ == "__main__":
    keep_alive()      # starts Flask server
    main()       # your telegram bot start function