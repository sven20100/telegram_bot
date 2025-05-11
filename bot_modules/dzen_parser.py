import logging
import requests
from bs4 import BeautifulSoup
from bot_modules.settings import DZEN_PROFILE_URLS, WEBSITE_CHECK_INTERVAL
from bot_modules.data_utils import save_post
import asyncio

logger = logging.getLogger(__name__)

async def check_dzen_website(bot):
    while True:
        for url in DZEN_PROFILE_URLS:
            try:
                logger.info(f"Парсинг URL: {url}")
                response = requests.get(url, timeout=15)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                posts = soup.find_all('article')
                for post in posts:
                    title = post.find('h2').text if post.find('h2') else "No title"
                    link = post.find('a')['href'] if post.find('a') else None
                    if link and not link.startswith('http'):
                        link = f"https://dzen.ru{link}"
                    if link:
                        save_post({"title": title, "link": link})
                        await bot.send_message(
                            chat_id=-1002684339596,
                            text=f"New post: {title}\n{link}"
                        )
            except Exception as e:
                logger.error(f"Ошибка парсинга {url}: {e}")
        await asyncio.sleep(WEBSITE_CHECK_INTERVAL)