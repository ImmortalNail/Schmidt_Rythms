from aiogram import types
from aiogram.dispatcher import Dispatcher
from keyboards import age_kb, routes_kb, route_confirm_kb
from texts import AGE_CONFIRM, AGE_DENY, NAME_REQUEST, WELCOME, ROUTES_PREVIEW, PROJECT_INFO, route_info
from database import save_user, update_user_route

dp = Dispatcher.get_current()

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer(AGE_CONFIRM, reply_markup=age_kb())

@dp.callback_query_handler(lambda c: c.data and c.data.startswith("age_"))
async def age_confirm(callback: types.CallbackQuery):
    if callback.data == "age_no":
        await callback.message.answer(AGE_DENY)
        await callback.answer()
    elif callback.data == "age_yes":
        await callback.message.answer(NAME_REQUEST)
        await callback.answer()

@dp.message_handler(lambda m: m.text and not m.photo)
async def get_name(message: types.Message):
    name = message.text.strip()
    await save_user(user_id=message.from_user.id, username=message.from_user.username, name=name)
    await message.answer(WELCOME.format(name=name))
    await message.answer(ROUTES_PREVIEW, parse_mode="Markdown")
    await message.answer(PROJECT_INFO, reply_markup=routes_kb())

@dp.callback_query_handler(lambda c: c.data and c.data.startswith("route_"))
async def choose_route(callback: types.CallbackQuery):
    route = callback.data.replace("route_", "")
    if route not in route_info:
        await callback.answer("Неверный маршрут, попробуйте снова.", show_alert=True)
        return

    await update_user_route(callback.from_user.id, route)
    text, img = route_info[route]
    await callback.message.answer_photo(photo=img, caption=text, parse_mode="Markdown", reply_markup=route_confirm_kb())
    await callback.answer()

@dp.callback_query_handler(lambda c: c.data == "confirm_route")
async def confirm_route(callback: types.CallbackQuery):
    await callback.message.answer("Отличный выбор! Теперь загрузи фото паспорта с отметкой из первого бара, чтобы подтвердить участие.")
    await callback.answer()

@dp.callback_query_handler(lambda c: c.data == "change_route")
async def change_route(callback: types.CallbackQuery):
    await callback.message.answer("Хорошо, выбери другой маршрут:", reply_markup=routes_kb())
    await callback.answer()