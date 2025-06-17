from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

def age_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Да", callback_data="age_yes")],
        [InlineKeyboardButton(text="Нет", callback_data="age_no")]
    ])

def routes_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Живой городской ритм", callback_data="route_urban")],
        [InlineKeyboardButton(text="Вечерний тусовочный ритм", callback_data="route_party")],
        [InlineKeyboardButton(text="Стильный современный ритм", callback_data="route_modern")],
        [InlineKeyboardButton(text="Летний солнечный ритм", callback_data="route_sunny")]
    ])

def route_confirm_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Выбрать другой маршрут", callback_data="routes")],
        [InlineKeyboardButton(text="Класс, я участвую", callback_data="join")]
    ])