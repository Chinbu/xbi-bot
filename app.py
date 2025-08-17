import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
from threading import Thread
from flask import Flask
import logging

# Set up logging for debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Get the bot token from environment variable
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    logger.error("BOT_TOKEN environment variable is not set!")
    raise ValueError("BOT_TOKEN environment variable is not set!")

# Handler for the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_message = (
        "Welcome to the TechYYrom Bot! 🎉\n"
        "Use /open to access the TechYY mini app."
    )
    await update.message.reply_text(welcome_message)
    logger.info("Sent welcome message to user %s", update.effective_user.id)

# Handler for the /open command
async def open_app(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Open TechYY Mini App", url='https://t.me/TechYYrom_bot/Techyy')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Click the button below to open the TechYY mini app!",
        reply_markup=reply_markup
    )
    logger.info("Sent open app button to user %s", update.effective_user.id)

def run_bot():
    try:
        # Create the Application instance
        application = Application.builder().token(BOT_TOKEN).build()
        # Register command handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("open", open_app))
        logger.info("Starting bot polling...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except Exception as e:
        logger.error("Bot failed to start: %s", str(e))
        raise

def run_web_server():
    flask_app = Flask(__name__)

    @flask_app.route('/')
    def health_check():
        return "Bot is alive!"

    # Use the PORT environment variable, default to 8080
    port = int(os.environ.get('PORT', 8080))
    logger.info("Starting Flask server on port %d", port)
    flask_app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    # Run the Flask server in a separate thread for health checks
    web_thread = Thread(target=run_web_server)
    web_thread.start()
    # Run the bot
    run_bot()
