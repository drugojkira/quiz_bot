import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from handlers.command_handlers import cmd_start, cmd_quiz
from handlers.callback_handlers import right_answer, wrong_answer
from db.database import create_table

API_TOKEN = 'Your_TOKEN'  # Замените на свой токен

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Регистрация хэндлеров
dp.message.register(cmd_start, Command("start"))
dp.message.register(cmd_quiz, F.text == "Начать игру")
dp.callback_query.register(right_answer, F.data.startswith("answer_"))
dp.callback_query.register(wrong_answer, F.data == "wrong_answer")


async def main():
    try:
        await create_table()
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
