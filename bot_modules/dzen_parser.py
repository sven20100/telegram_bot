import logging
import aiohttp
from bs4 import BeautifulSoup
from bot_modules.data_utils import save_post
from bot_modules.publish import publish_to_channel
from bot_modules.settings import DZEN_PROFILE_URLS

logger = logging.getLogger(__name__)

async def check_dzen_website(context):
    for url in DZEN_PROFILE_URLS:
        logger.info(f"Парсинг URL: {url}")
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, timeout=10) as response:
                    response.raise_for_status()
                    soup = BeautifulSoup(await response.text(), 'html.parser')
                    posts = soup.find_all('div', class_='card-image-feed')  # Новый селектор
                    posts_data = []
                    for post in posts:
                        title = post.find('h2').text if post.find('h2') else ""
                        link = post.find('a')['href'] if post.find('a') else ""
                        if title and link:
                            posts_data.append({"title": title, "link": f"https://dzen.ru{link}" if link.startswith('/') else link})
                    if not posts_data:
                        logger.info("Посты не найдены")
                    for post in posts_data:
                        await save_post(post)
                        await publish_to_channel(context, post)
                        logger.info(f"Сохранён и опубликован пост: {post['title'][:50]}...")
            except Exception as e:
                logger.error(f"Ошибка парсинга {url}: {e}")