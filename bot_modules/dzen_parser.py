import logging
import aiohttp
from bot_modules.data_utils import save_post
from bot_modules.publish import publish_to_channel
from bot_modules.settings import DZEN_PROFILE_URLS, DZEN_TOKEN

logger = logging.getLogger(__name__)

async def check_dzen_website(context):
    for url in DZEN_PROFILE_URLS:
        logger.info(f"Парсинг URL: {url}")
        async with aiohttp.ClientSession() as session:
            try:
                # Пример: Используем API Дзена (нужен правильный эндпоинт)
                api_url = "https://api.dzen.ru/v3/news"  # Проверить актуальный API
                headers = {"Authorization": f"Bearer {DZEN_TOKEN}"}
                async with session.get(api_url, headers=headers, timeout=10) as response:
                    response.raise_for_status()
                    data = await response.json()
                    posts_data = []
                    # Предполагаемая структура ответа API
                    for item in data.get("items", []):
                        title = item.get("title", "")
                        link = item.get("url", "")
                        if title and link:
                            posts_data.append({"title": title, "link": link})
                    if not posts_data:
                        logger.info("Посты не найдены")
                    for post in posts_data:
                        await save_post(post)
                        await publish_to_channel(context, post)
                        logger.info(f"Сохранён и опубликован пост: {post['title'][:50]}...")
            except Exception as e:
                logger.error(f"Ошибка парсинга {url}: {e}")