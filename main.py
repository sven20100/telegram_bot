import asyncio
import logging
import warnings
from telegram import Bot
from telegram.ext import Application, CommandHandler
from telegram.warnings import PTBUserWarning
from bot_modules.handlers import start, menu, admin_panel, search_posts
from bot_modules.dzen_parser import check_dzen_website
from bot_modules.settings import TELEGRAM_TOKEN

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

warnings.filterwarnings("ignore", category=PTBUserWarning)

async def main():
    logger.info("Bot is starting...")
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", menu))
    application.add_handler(CommandHandler("admin", admin_panel))
    application.add_handler(CommandHandler("search", search_posts))

    bot = Bot(token=TELEGRAM_TOKEN)
    asyncio.create_task(check_dzen_website(bot))

    await application.run_polling()
    logger.info("Application started")

if __name__ == '__main__':
    asyncio.run(main())