import logging
import aiohttp
from telegram import Bot
from bot_modules.settings import TARGET_CHANNEL_ID, DZEN_TOKEN

logger = logging.getLogger(__name__)

async def publish_to_channel(context, post):
    try:
        await context.bot.send_message(
            chat_id=TARGET_CHANNEL_ID,
            text=f"{post['title']}\n{post['link']}"
        )
        logger.info(f"Переслано сообщение в Telegram: {post['title'][:50]}...")
    except Exception as e:
        logger.error(f"Ошибка пересылки в Telegram: {e}", exc_info=True)

async def publish_to_dzen(post):
    try:
        api_url = "https://api.dzen.ru/v3/articles"  # Предполагаемый эндпоинт
        headers = {"Authorization": f"Bearer {DZEN_TOKEN}"}
        payload = {
            "title": post["title"],
            "url": post["link"],
            "content": post.get("content", post["title"])
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(api_url, headers=headers, json=payload) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(f"Ошибка публикации в Дзен: {response.status} {error_text}")
                    return
                logger.info(f"Опубликован в Дзен: {post['title'][:50]}...")
    except Exception as e:
        logger.error(f"Ошибка публикации в Дзен: {e}", exc_info=True)