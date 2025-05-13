# bot_modules/dzen_parser.py
import httpx
import logging

logger = logging.getLogger(__name__)

async def check_dzen_website():
    logger.info("Парсинг API: https://api.dzen.ru/v3/feed?category=auto")
    try:
        # Настройка прокси (раскомментируйте и укажите ваш прокси, если нужен)
        # proxies = {"https": "http://your_proxy:port"}
        async with httpx.AsyncClient(timeout=30, proxies=None) as client:
            response = await client.get("https://api.dzen.ru/v3/feed?category=auto")
            response.raise_for_status()
            logger.info("Парсинг успешен")
            # Добавьте вашу логику обработки ответа, например:
            # data = response.json()
            # logger.info(f"Получено: {data}")
    except httpx.TimeoutException as e:
        logger.error(f"Таймаут при запросе к API Дзена: {e}")
    except httpx.HTTPStatusError as e:
        logger.error(f"Ошибка HTTP при запросе к API Дзена: {e}, статус: {e.response.status_code}")
    except httpx.RequestError as e:
        logger.error(f"Сетевая ошибка при запросе к API Дзена: {e}")
    except Exception as e:
        logger.error(f"Общая ошибка парсинга Дзена: {e}")