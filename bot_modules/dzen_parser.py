async def check_dzen_website(context):
    url = "https://dzen.ru/id/680e334acbb89444e26a3bd2"
    logger.info(f"Парсинг URL: {url}")
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=10) as response:
                response.raise_for_status()
                soup = BeautifulSoup(await response.text(), 'html.parser')
                posts = soup.find_all('div', class_='card')
                posts_data = []
                for post in posts:
                    title = post.find('h2').text if post.find('h2') else ""
                    link = post.find('a')['href'] if post.find('a') else ""
                    if title and link:
                        posts_data.append({"title": title, "link": link})
                for post in posts_data:
                    await save_post(post)
                    logger.info(f"Сохранён пост: {post['title'][:50]}...")
        except Exception as e:
            logger.error(f"Ошибка парсинга {url}: {e}")