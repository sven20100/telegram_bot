import logging
import asyncio
import requests
from bs4 import BeautifulSoup
from bot_modules.data_utils import save_post

logger = logging.getLogger(__name__)

async def check_dzen_website(bot):
    url = "https://dzen.ru/id/680e334acbb89444e26a3bd2"
    logger.info(f"Парсинг URL: {url}")
    while True:
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            posts = []  # Дополни логику парсинга
            for post in posts:
                await save_post(post)
        except Exception as e:
            logger.error(f"Ошибка парсинга: {e}")
        await asyncio.sleep(3600)  # Пауза 1 час