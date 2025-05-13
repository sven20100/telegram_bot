# bot_modules/handlers.py
import logging
from telegram.ext import Application

# Настройка логирования
logger = logging.getLogger(__name__)

# Конфигурация (дублируем, если нужно)
ADMIN_IDS = [6503798414]  # Замените на ваши ID администраторов
CHANNEL_ID = -1002684339596  # Замените на ваш ID канала

async def start(update, context):
    logger.info("Команда /start получена")
    try:
        await update.message.reply_text("Бот запущен!")
    except Exception as e:
        logger.error(f"Ошибка в /start: {e}")

async def admin(update, context):
    user_id = update.effective_user.id
    logger.info(f"Попытка доступа к /admin, user_id: {user_id}")
    try:
        if user_id in ADMIN_IDS:
            await update.message.reply_text("Добро пожаловать в админ-панель!")
        else:
            await update.message.reply_text("Доступ запрещён.")
    except Exception as e:
        logger.error(f"Ошибка в /admin: {e}")

async def handle_message(update, context):
    user_id = update.effective_user.id
    text = update.message.text
    logger.info(f"Получено сообщение от user_id: {user_id}, текст: {text}")
    try:
        if user_id in ADMIN_IDS:
            await context.bot.send_message(
                chat_id=CHANNEL_ID,
                text=f"{text}..."
            )
            logger.info(f"Переслано сообщение в {CHANNEL_ID}: {text}...")
        else:
            await update.message.reply_text("Вы не администратор.")
    except Exception as e:
        logger.error(f"Ошибка при пересылке сообщения: {e}")
        await update.message.reply_text("Ошибка при обработке сообщения.")