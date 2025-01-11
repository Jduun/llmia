import os

from dotenv import load_dotenv
import asyncio
import logging
from aiogram import Bot, Dispatcher

from handlers import router

load_dotenv()
bot: Bot = Bot(token=os.getenv("TG_TOKEN"))

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(filename)s:%(lineno)d #%(levelname)-8s "
    "[%(asctime)s] - %(name)s - %(message)s",
)

logger.info("Starting bot")

dp: Dispatcher = Dispatcher()
dp.include_router(router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")
