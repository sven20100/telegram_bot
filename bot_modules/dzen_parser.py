import logging
import aiohttp
from bot_modules.data_utils import save_post
from bot_modules.publish import publish_to_channel, publish_to_dzen
from bot_modules.settings import DZEN_TOKEN

logger = logging.getLogger(__name__)

async def check_dzen_website(context):
    api_url = "https://api.dzen.ru/v3/feed?category=auto"
    logger.info(f"Парсинг API: {api_url}")
    async with aiohttp.ClientSession() as session:
        try:
            headers = {"Authorization": f"Bearer {DZEN_TOKEN}"}
            async with session.get(api_url, headers=headers, timeout=15) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(f"API вернул ошибку: {response.status} {error_text}")
                    return
                data = await response.json()
                logger.info(f"Получен ответ API: {data}")
                posts_data = []
                items = data.get("items", []) or data.get("feed", []) or data.get("data", [])
                for item in items:
                    title = item.get("title", "") or item.get("name", "")
                    link = item.get("url", "") or item.get("link", "")
                    if title and link:
                        posts_data.append({"title": title, "link": link})
                if not posts_data:
                    logger.info("Посты не найдены")
                else:
                    logger.info(f"Найдено постов: {len(posts_data)}")
                for post in posts_data:
                    await save_post(post)
                    await publish_to_channel(context, post)
                    await publish_to_dzen(post)
                    logger.info(f"Сохранён и опубликован пост: {post['title'][:50]}...")
        except aiohttp.ClientError as e:
            logger.error(f"Ошибка сети при запросе к API: {e}")
        except Exception as e:
            logger.error(f"Ошибка парсинга API: {e}", exc_info=True)