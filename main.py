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
        if application.running:
            try:
                await application.stop()
            except Exception as stop_error:
                logger.error(f"Ошибка при остановке бота: {stop_error}")
    finally:
        try:
            logger.info("Stopping application...")
            await application.shutdown()
            logger.info("Application stopped")
        except Exception as shutdown_error:
            logger.error(f"Ошибка при завершении работы: {shutdown_error}")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")