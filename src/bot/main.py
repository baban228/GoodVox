import asyncio
import logging
from telegram.ext import ApplicationBuilder
from config.settings import TELEGRAM_BOT_TOKEN

from src.bot.handlers.init_handlers import setup_handlers

logging.basicConfig(
    format='-> %(asctime)s %(levelname)s: [%(name)s] %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self):
        self.app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
        setup_handlers(self.app)

    async def post_init(self, application):
        """Функция, вызываемая после инициализации приложения"""
        logger.info("Бот успешно запущен!")
        logger.info("Ожидание сообщений...")

    async def run(self):
        self.app.post_init = self.post_init
        logger.info("Бот запущен...")
        async with self.app:
            await self.app.start()
            await self.app.updater.start_polling()
            await asyncio.Event().wait()

async def main():
    bot = TelegramBot()
    await bot.run()

if __name__ == "__main__":
    asyncio.run(main())