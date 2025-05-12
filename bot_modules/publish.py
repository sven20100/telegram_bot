import logging
from telegram.error import TelegramError
from bot_modules.settings import TARGET_CHANNEL_ID

logger = logging.getLogger(__name__)

async def publish_to_channel(context, post):
    try:
        await context.bot.send_message(
            chat_id=TARGET_CHANNEL_ID,
            text=f"{post['title']}\n{post['link']}"
        )
        logger.info(f"Опубликован пост в {TARGET_CHANNEL_ID}: {post['title'][:50]}...")
    except TelegramError as e:
        logger.error(f"Ошибка публикации в {TARGET_CHANNEL_ID}: {e}")