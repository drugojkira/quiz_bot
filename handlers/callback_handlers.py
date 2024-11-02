from aiogram import types
from aiogram.types import CallbackQuery
from models.quiz_data import quiz_data
from db.database import get_quiz_index, update_quiz_index, save_quiz_result

# Счетчики правильных и неправильных ответов
correct_answers_count = 0
incorrect_answers_count = 0


async def generate_options_keyboard(options):
    """Генерирует клавиатуру с вариантами ответов."""
    buttons = [
        types.InlineKeyboardButton(
            text=option, callback_data=f"answer_{index}"
        )
        for index, option in enumerate(options)
    ]

    keyboard = [buttons]
    return types.InlineKeyboardMarkup(inline_keyboard=keyboard)


async def right_answer(callback: CallbackQuery):
    global correct_answers_count
    selected_answer_index = int(callback.data.split("_")[1])
    current_question_index = await get_quiz_index(callback.from_user.id)

    if selected_answer_index == quiz_data[current_question_index]['correct_option']:
        correct_answers_count += 1
        await callback.answer("Верно!")
        await callback.message.answer("Верно!")
    else:
        await wrong_answer(callback)

    await next_question(callback)


async def wrong_answer(callback: CallbackQuery):
    global incorrect_answers_count
    incorrect_answers_count += 1

    await callback.answer("Неправильно.")
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    current_question_index = await get_quiz_index(callback.from_user.id)
    correct_option = quiz_data[current_question_index]['correct_option']
    await callback.message.answer(
        f"Неправильно. Правильный ответ: {quiz_data[current_question_index]['options'][correct_option]}"
    )

    await next_question(callback)


async def next_question(callback: CallbackQuery):
    global correct_answers_count, incorrect_answers_count
    current_question_index = await get_quiz_index(callback.from_user.id)

    if current_question_index + 1 < len(quiz_data):
        current_question_index += 1
        await update_quiz_index(callback.from_user.id, current_question_index)
        await get_question(callback.message, callback.from_user.id)
    else:
        # Сохраняем результаты квиза
        await save_quiz_result(
            callback.from_user.id,
            current_question_index,
            correct_answers_count,
            incorrect_answers_count
        )
        await callback.message.answer(
            f"Это был последний вопрос. Квиз завершен! "
            f"Правильные ответы: {correct_answers_count}, "
            f"Неправильные ответы: {incorrect_answers_count}"
        )

        # Сбросим счетчики
        correct_answers_count = 0
        incorrect_answers_count = 0


async def get_question(message: types.Message, user_id: int):
    current_question_index = await get_quiz_index(user_id)

    if current_question_index < len(quiz_data):
        opts = quiz_data[current_question_index]['options']
        kb = await generate_options_keyboard(opts)
        await message.answer(f"{quiz_data[current_question_index]['question']}", reply_markup=kb)
    else:
        await message.answer(
            "Квиз завершен или произошла ошибка. Пожалуйста, попробуйте снова."
        )
