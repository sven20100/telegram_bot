import json
import aiofiles
import logging

logger = logging.getLogger(__name__)

async def save_post(post):
    try:
        async with aiofiles.open('posts.json', 'a', encoding='utf-8') as f:
            await f.write(json.dumps(post, ensure_ascii=False) + '\n')
        logger.info(f"Пост сохранён: {post['title'][:50]}...")
    except Exception as e:
        logger.error(f"Ошибка сохранения поста: {e}")