# bot_modules/dzen_parser.py
import httpx
import logging

logger = logging.getLogger(__name__)  # Corrected logger initialization

async def check_dzen_website():
    logger.info("Парсинг API: https://api.dzen.ru/v3/feed?category=auto")
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get("https://api.dzen.ru/v3/feed?category=auto")
            response.raise_for_status()
            # Add your response processing logic here
            logger.info("Парсинг успешен")
    except httpx.HTTPError as e:
        logger.error(f"Ошибка сети при запросе к API Дзена: {e}")
    except Exception as e:
        logger.error(f"Общая ошибка парсинга: {e}")