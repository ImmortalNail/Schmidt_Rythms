import logging
import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os
from handlers import register_handlers
from admin import router as admin_router
from database import init_db
from scheduler import schedule

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def main():
    await init_db()
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    dp.include_router(admin_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())