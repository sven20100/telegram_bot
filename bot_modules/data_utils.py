import json
import logging

logger = logging.getLogger(__name__)

def save_post(post):
    try:
        with open('posts.json', 'a', encoding='utf-8') as f:
            json.dump(post, f, ensure_ascii=False)
            f.write('\n')
        logger.info(f"Сохранён пост: {post['title']}")
    except Exception as e:
        logger.error(f"Ошибка сохранения поста: {e}")