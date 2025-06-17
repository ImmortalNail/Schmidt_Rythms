from aiogram import Router, types, F
from aiogram.filters import Command
from dotenv import load_dotenv
import os
from database import get_all_users, get_top_users

load_dotenv()
admin_router = Router()
ADMINS = list(map(int, os.getenv("ADMIN_IDS", "").split(",")))

@admin_router.message(Command("broadcast"))
async def broadcast(message: types.Message):
    if message.from_user.id not in ADMINS:
        return
    text = message.text.split(" ", 1)[-1]
    users = await get_all_users()
    for user in users:
        try:
            await message.bot.send_message(user[0], text)
        except:
            continue

@admin_router.message(Command("top30"))
async def send_top30(message: types.Message):
    if message.from_user.id not in ADMINS:
        return
    top_users = await get_top_users()
    for uid in top_users:
        try:
            await message.bot.send_message(uid, "🎉 Ты в топ-30 участников! Ждём тебя на закрытой вечеринке!")
        except:
            continue

@admin_router.message(Command("export"))
async def export(message: types.Message):
    if message.from_user.id not in ADMINS:
        return
    users = await get_all_users()
    text = "ID, Username, Name, Route, Photo Count\n"
    for user in users:
        text += f"{user[0]},{user[1]},{user[2]},{user[3]},{user[6]}\n"
    await message.answer_document(types.InputFile.from_string(text, filename="participants.csv"))