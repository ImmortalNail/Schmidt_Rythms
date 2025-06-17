import os
from aiogram.types import Message
from uuid import uuid4

async def save_photo(message: Message):
    photo = message.photo[-1]
    file = await message.bot.get_file(photo.file_id)
    path = f"photos/{uuid4()}.jpg"
    os.makedirs("photos", exist_ok=True)
    await message.bot.download_file(file.file_path, path)
    return path