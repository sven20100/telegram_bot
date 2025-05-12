import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from bot_modules.settings import ADMIN_IDS
import json

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот для кросспостинга. Используй /menu для навигации.")

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Поиск постов", callback_data='search')],
        [InlineKeyboardButton("Админ-панель", callback_data='admin')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Главное меню:", reply_markup=reply_markup)

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id if update.effective_user else None
    logger.info(f"Попытка доступа к /admin, user_id: {user_id}, ADMIN_IDS: {ADMIN_IDS}")
    if user_id in ADMIN_IDS:
        keyboard = [
            [InlineKeyboardButton("Показать статистику", callback_data="show_stats")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Админ-панель:", reply_markup=reply_markup)
    else:
        await update.message.reply_text("Доступ запрещён.")

async def search_posts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyword = ' '.join(context.args)
    if not keyword:
        await update.message.reply_text("Укажите ключевое слово: /search <keyword>")
        return
    try:
        with open('posts.json', 'r', encoding='utf-8') as f:
            posts = [json.loads(line) for line in f]
        results = [post for post in posts if keyword.lower() in post['title'].lower()]
        if results:
            response = "\n".join([f"{post['title']}: {post['link']}" for post in results])
            await update.message.reply_text(response)
        else:
            await update.message.reply_text("Посты не найдены.")
    except Exception as e:
        await update.message.reply_text(f"Ошибка поиска: {e}")