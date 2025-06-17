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
    logging.basicConfig(level=logging.INFO)
    await init_db()
    register_handlers(dp)
    dp.include_router(admin_router)
    asyncio.create_task(schedule(bot))
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())