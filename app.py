import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from flask import Flask, request, Response
import logging
import asyncio

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize Flask app
flask_app = Flask(__name__)

# Get environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')
KOYEB_EXTERNAL_URL = os.getenv('KOYEB_EXTERNAL_URL')

if not BOT_TOKEN:
    logger.error("BOT_TOKEN environment variable is not set!")
    raise ValueError("BOT_TOKEN environment variable is not set!")
if not KOYEB_EXTERNAL_URL:
    logger.error("KOYEB_EXTERNAL_URL environment variable is not set!")
    raise ValueError("KOYEB_EXTERNAL_URL environment variable is not set!")

# Handler for /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_message = "Welcome to the TechYYrom Bot! 🎉"
    await update.message.reply_text(welcome_message)
    logger.info("Sent welcome message to user %s", update.effective_user.id)

# Flask route for webhook
@flask_app.route('/telegram', methods=['POST'])
async def telegram_webhook():
    try:
        update = Update.de_json(request.get_json(), application.bot)
        await application.process_update(update)
        return Response(status=200)
    except Exception as e:
        logger.error("Webhook error: %s", str(e))
        return Response(status=500)

# Flask route for health check
@flask_app.route('/')
def health_check():
    return "Bot is alive!"

async def main():
    try:
        # Create Application instance
        global application
        application = Application.builder().token(BOT_TOKEN).updater(None).build()

        # Register /start handler
        application.add_handler(CommandHandler("start", start))

        # Set webhook
        webhook_url = f"{KOYEB_EXTERNAL_URL}/telegram"
        logger.info(f"Setting webhook to {webhook_url}")
        await application.bot.set_webhook(url=webhook_url, allowed_updates=Update.ALL_TYPES)

        # Start Flask
        port = int(os.environ.get('PORT', 8080))
        logger.info(f"Starting Flask server on port {port}")
        flask_app.run(host='0.0.0.0', port=port, debug=False)
    except Exception as e:
        logger.error("Bot failed to start: %s", str(e))
        raise

if __name__ == '__main__':
    asyncio.run(main())
