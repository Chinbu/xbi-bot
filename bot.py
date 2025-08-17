import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
from threading import Thread
from flask import Flask

# Get the bot token from environment variable
BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is not set!")

# Handler for the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_message = (
        "Welcome to the TechYYrom Bot! 🎉\n"
        "Use /open to access the TechYY mini app."
    )
    await update.message.reply_text(welcome_message)

# Handler for the /open command
async def open_app(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Create an inline keyboard with a button that links to the mini app
    keyboard = [
        [InlineKeyboardButton("Open TechYY Mini App", url='https://t.me/TechYYrom_bot/Techyy')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Send a message with the button
    await update.message.reply_text(
        "Click the button below to open the TechYY mini app!",
        reply_markup=reply_markup
    )

def main() -> None:
    # Create the Application instance
    application = Application.builder().token(BOT_TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("open", open_app))

    # Start the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

def run_web_server():
    flask_app = Flask(__name__)

    @flask_app.route('/')
    def health_check():
        return "Bot is alive!"

    port = int(os.environ.get('PORT', 8080))
    flask_app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    # Run the web server in a separate thread for health checks
    web_thread = Thread(target=run_web_server)
    web_thread.start()

    # Run the main bot polling
    main()
