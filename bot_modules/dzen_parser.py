async def check_dzen_website(bot):
    url = "https://dzen.ru/id/680e334acbb89444e26a3bd2"
    logger.info(f"Парсинг URL: {url}")
    while True:
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            # Логика парсинга (дополни по своему коду)
            posts = [...]  # Извлечение постов
            for post in posts:
                await save_post(post)
        except Exception as e:
            logger.error(f"Ошибка парсинга: {e}")
        await asyncio.sleep(3600)  # Пауза 1 час