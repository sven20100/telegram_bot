import logging
import warnings
from telegram.ext import Application, CommandHandler
from telegram.warnings import PTBUserWarning
from bot_modules.handlers import start, menu, admin_panel, search_posts
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
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", menu))
    application.add_handler(CommandHandler("admin", admin_panel))
    application.add_handler(CommandHandler("search", search_posts))

    # Запускаем парсинг как повторяющуюся задачу
    # application.job_queue.run_repeating(check_dzen_website, interval=3600, first=15)

    application.run_polling()
    logger.info("Application started")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Ошибка: {e}")