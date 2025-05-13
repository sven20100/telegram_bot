# main.py
import asyncio
import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram.error import Conflict, NetworkError
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from lockfile import LockFile, LockTimeout
from bot_modules.handlers import start, admin, handle_message
from bot_modules.dzen_parser import check_dzen_website

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Конфигурация
TOKEN = "7938456191:AAG14pZ0Dqw2BSSy_YvCz5axtRXHMcLhZUc"  # Ваш реальный токен
ADMIN_IDS = [6503798414]  # Замените на ваши ID администраторов
CHANNEL_ID = -1002684339596  # Замените на ваш ID канала

# Обработчик ошибок
async def error_handler(update, context):
    logger.error(f"Ошибка: {context.error}")
    if isinstance(context.error, Conflict):
        logger.error("Конфликт getUpdates. Завершаю приложение...")
        await context.application.updater.stop()
        await context.application.stop()
        await context.application.shutdown()
        raise context.error
    elif isinstance(context.error, NetworkError):
        logger.warning(f"Сетевая ошибка Telegram: {context.error}. Продолжаю работу...")
    else:
        logger.warning(f"Необработанная ошибка: {context.error}")

async def main():
    logger.info("Запуск бота...")
    app = None
    scheduler = None
    try:
        # Инициализация приложения
        app = Application.builder().token(TOKEN).build()
        logger.info("Application инициализировано")

        # Регистрация обработчиков
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("admin", admin))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        app.add_error_handler(error_handler)
        logger.info("Обработчики зарегистрированы")

        # Настройка планировщика
        scheduler = AsyncIOScheduler()
        scheduler.add_job(check_dzen_website, "interval", seconds=60)
        logger.info("Планировщик настроен для check_dzen_website")
        scheduler.start()

        # Запуск приложения
        await app.initialize()
        await app.start()
        logger.info("Application запущено")
        await app.updater.start_polling(drop_pending_updates=True)

        # Бесконечное ожидание
        await asyncio.Event().wait()

    except Exception as e:
        logger.error(f"Ошибка в main: {e}")
        raise
    finally:
        logger.info("Завершение работы...")
        if scheduler:
            scheduler.shutdown()
            logger.info("Планировщик остановлен")
        if app:
            if app.updater.running:
                await app.updater.stop()
                logger.info("Updater остановлен")
            await app.stop()
            await app.shutdown()
            logger.info("Application остановлено")

if __name__ == "__main__":
    logger.info("Проверка на единственный экземпляр...")
    lock = LockFile("bot.lock", timeout=5)
    try:
        with lock:
            asyncio.run(main())
    except LockTimeout:
        logger.error("Другой экземпляр бота уже запущен! Завершаю...")
        exit(1)
    except KeyboardInterrupt:
        logger.info("Получен сигнал прерывания")
        exit(0)
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
        exit(1)