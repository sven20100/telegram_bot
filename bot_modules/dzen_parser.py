import logging
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from bot_modules.data_utils import save_post

logger = logging.getLogger(__name__)

async def check_dzen_website(context):
    url = "https://dzen.ru/id/680e334acbb89444e26a3bd2"
    logger.info(f"Парсинг URL: {url}")
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with session.get(url, timeout=10) as response:
                    response.raise_for_status()
                    soup = BeautifulSoup(await response.text(), 'html.parser')
                    posts = soup.find_all('div', class_='card')  # Обнови селектор
                    posts_data = []
                    for post in posts:
                        title = post.find('h2').text if post.find('h2') else ""
                        link = post.find('a')['href'] if post.find('a') else ""
                        posts_data.append({"title": title, "link": link})
                    for post in posts_data:
                        await save_post(post)
            except Exception as e:
                logger.error(f"Ошибка парсинга: {e}")
            await asyncio.sleep(3600)  # Пауза 1 час