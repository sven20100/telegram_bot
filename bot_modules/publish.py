import logging
from telegram import Bot
from bot_modules.settings import TARGET_CHANNEL_ID

logger = logging.getLogger(__name__)

async def publish_post(bot: Bot, post):
    try:
        await bot.send_message(
            chat_id=TARGET_CHANNEL_ID,
            text=f"New post: {post['title']}\n{post['link']}"
        )
        logger.info(f"Опубликован пост: {post['title']}")
    except Exception as e:
        logger.error(f"Ошибка публикации: {e}")