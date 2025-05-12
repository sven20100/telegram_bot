import logging
import warnings
import telegram
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram.warnings import PTBUserWarning
from bot_modules.handlers import start, menu, admin_panel, search_posts, handle_text
from bot_modules.dzen_parser import check_dzen_website
from bot_modules.settings import TELEGRAM_TOKEN

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

warnings.filterwarnings("ignore", category=PTBUserWarning)

def main():
    logger.info("Bot is starting...")
    logger.info(f"python-telegram-bot version: {telegram.__version__}")
    if not TELEGRAM_TOKEN:
        logger.error("TELEGRAM_TOKEN is not set in settings.py")
        return
    try:
        application = Application.builder().token(TELEGRAM_TOKEN).build()
        logger.info("Application initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize application: {e}")
        return

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", menu))
    application.add_handler(CommandHandler("admin", admin_panel))
    application.add_handler(CommandHandler("search", search_posts))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    if application.job_queue is None:
        logger.error("Job queue is not initialized")
        return
    application.job_queue.run_repeating(check_dzen_website, interval=3600, first=15)
    logger.info("Job queue scheduled for check_dzen_website")

    application.run_polling(allowed_updates=["message", "callback_query"])
    logger.info("Application started")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Ошибка: {e}")