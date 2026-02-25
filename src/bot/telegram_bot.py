# from telegram import Update
# from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters


from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import os

def start_telegram_bot(on_message_callback):
    """
    Starts Telegram bot.

    on_message_callback:
        function that takes (message: str) -> str
    """
    BOT_TOKEN = "8176147181:AAHiBIMf_TaT0YN0gHxLOuJWldGkaod2yzw"

    # BOT_TOKEN = BOT_TOKEN

    if not BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN not set")

    async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.message or not update.message.text:
            return

        user_text = update.message.text
        print("[Telegram] Message received:", user_text)

        try:
            # Pass message to main.py logic
            response = on_message_callback(user_text)

            # Send response back
            await update.message.reply_text(response)

        except Exception as e:
            print("[Telegram] Error:", e)
            await update.message.reply_text(
                "❌ Error while processing your message."
            )

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    print("[Telegram] Bot started...")
    app.run_polling()
