import asyncio
import aiosqlite
from datetime import datetime, timedelta
from aiogram import Bot
from database import get_all_users

async def send_reminders(bot: Bot):
    now = datetime.utcnow()
    users = await get_all_users()
    for user in users:
        user_id, username, name, route, photo_path, created_at, photo_count = user
        if created_at:
            reg_time = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
            if (now - reg_time).days == 3 and not photo_path:
                try:
                    await bot.send_message(user_id, "👋 Напоминаем, что нужно загрузить фото паспорта для участия в бар-туре!")
                except:
                    continue

async def schedule(bot: Bot):
    while True:
        await send_reminders(bot)
        await asyncio.sleep(86400)