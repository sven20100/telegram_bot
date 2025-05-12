import logging
import warnings
import asyncio
from telegram import Update  # Добавляем этот импорт
from telegram.ext import Application, CommandHandler
from telegram.warnings import PTBUserWarning
from bot_modules.handlers import start, menu, admin_panel, search_posts
from bot_modules.dzen_parser import check_dzen_website
from bot_modules.settings import TELEGRAM_TOKEN

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

warnings.filterwarnings("ignore", category=PTBUserWarning)

async def main():
    logger.info("Bot is starting...")
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", menu))
    application.add_handler(CommandHandler("admin", admin_panel))
    application.add_handler(CommandHandler("search", search_posts))

    logger.info("Application starting...")
    try:
        await application.initialize()
        await application.start()
        logger.info("Application started")
        await application.run_polling(drop_pending_updates=True)
    except Exception as e:
        logger.error(f"Ошибка при работе бота: {e}")
    finally:
        logger.info("Stopping application...")
        if application.running:
            await application.stop()  # Ensure this is awaited
        await application.shutdown()  # Ensure this is awaited
        logger.info("Application stopped")

if __name__ == '__main__':
    try:
        policy = asyncio.WindowsSelectorEventLoopPolicy()
        asyncio.set_event_loop_policy(policy)
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")