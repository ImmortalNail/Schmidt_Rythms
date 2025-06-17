from aiogram import types
from aiogram.dispatcher import Dispatcher
from database import get_all_users, get_top_users
import os

dp = Dispatcher.get_current()
ADMINS = list(map(int, os.getenv("ADMIN_IDS", "").split(",")))

def is_admin(user_id):
    return user_id in ADMINS

@dp.message_handler(commands=['broadcast'])
async def broadcast(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    text = message.text.partition(' ')[2]
    users = await get_all_users()
    for user in users:
        try:
            await message.bot.send_message(user[0], text)
        except:
            pass

@dp.message_handler(commands=['top30'])
async def send_top30(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    top_users = await get_top_users()
    for uid in top_users:
        try:
            await message.bot.send_message(uid, "🎉 Ты в топ-30 участников! Ждём тебя на закрытой вечеринке!")
        except:
            pass

@dp.message_handler(commands=['export'])
async def export(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    users = await get_all_users()
    text = "ID,Username,Name,Route,Photo Count\n"
    for user in users:
        text += f"{user[0]},{user[1]},{user[2]},{user[3]},{user[6]}\n"
    await message.answer_document(types.InputFile.from_string(text, filename="participants.csv"))