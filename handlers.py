from aiogram import Router, types, F
from aiogram.filters import CommandStart
from keyboards import age_kb, routes_kb, route_confirm_kb, yes_no_kb
from texts import AGE_CONFIRM, AGE_DENY, NAME_REQUEST, WELCOME, ROUTES_PREVIEW, PROJECT_INFO, route_info
from database import save_user, update_user_route
from aiogram.types import Message, CallbackQuery

router = Router()

# 1. Старт и запрос подтверждения возраста
@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(AGE_CONFIRM, reply_markup=age_kb())

# 2. Обработка ответа по возрасту
@router.callback_query(F.data.startswith("age_"))
async def age_handler(callback: CallbackQuery):
    if callback.data == "age_no":
        await callback.message.answer(AGE_DENY)
        await callback.answer()
        # Можно здесь сделать отключение пользователя или как-то завершить диалог
    else:
        await callback.message.answer(NAME_REQUEST)
        await callback.answer()

# 3. Получение имени пользователя (после подтверждения возраста)
@router.message(lambda msg: msg.text and not msg.photo)
async def get_name(message: Message):
    name = message.text.strip()
    await save_user(user_id=message.from_user.id, username=message.from_user.username, name=name)
    await message.answer(WELCOME.format(name=name))
    await message.answer(ROUTES_PREVIEW, parse_mode="Markdown")
    await message.answer(PROJECT_INFO, reply_markup=routes_kb())

# 4. Выбор маршрута пользователем
@router.callback_query(F.data.startswith("route_"))
async def choose_route(callback: CallbackQuery):
    route = callback.data.replace("route_", "")
    if route not in route_info:
        await callback.answer("Неверный маршрут, попробуйте снова.", show_alert=True)
        return

    await update_user_route(callback.from_user.id, route)
    text, img = route_info[route]
    await callback.message.answer_photo(photo=img, caption=text, parse_mode="Markdown", reply_markup=route_confirm_kb())
    await callback.answer()

# 5. Подтверждение маршрута
@router.callback_query(F.data == "confirm_route")
async def confirm_route(callback: CallbackQuery):
    await callback.message.answer("Отличный выбор! Теперь загрузи фото паспорта с отметкой из первого бара, чтобы подтвердить участие.")
    await callback.answer()

@router.callback_query(F.data == "change_route")
async def change_route(callback: CallbackQuery):
    await callback.message.answer("Хорошо, выбери другой маршрут:", reply_markup=routes_kb())
    await callback.answer()