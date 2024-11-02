from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from handlers.callback_handlers import get_question
from db.database import update_quiz_index


async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Начать игру"))
    await message.answer(
        "Добро пожаловать в квиз!",
        reply_markup=builder.as_markup(resize_keyboard=True)
    )


async def cmd_quiz(message: types.Message):
    await message.answer("Давайте начнем квиз!")
    user_id = message.from_user.id
    await update_quiz_index(user_id, 0)
    await get_question(message, user_id)
