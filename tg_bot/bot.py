import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from application.database import init_db
from const import API_TOKEN, REDIS_URL
from tg_bot.handlers import router

logging.basicConfig(level=logging.INFO)


async def main():
    dp = Dispatcher(storage=RedisStorage.from_url(REDIS_URL))
    dp.include_router(router)

    await init_db()
    await dp.start_polling(Bot(token=API_TOKEN), skip_updates=True)


if __name__ == '__main__':
    asyncio.run(main())
