
# Quiz Bot

## Описание

Это Telegram-бот для проведения квизов. Пользователи могут отвечать на вопросы и получать результаты.

## Установка

1. Создайте виртуальное окружение:

   ```bash
   python -m venv venv
   ```

2. Активируйте виртуальное окружение:

   - На Windows:
     ```bash
     venv\Scripts\activate
     ```

   - На macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

3. Установите зависимости:

   ```bash
   pip install -r requirements.txt
   ```

4. Замените `YOUR_BOT_TOKEN` в файле `main.py` на токен вашего бота, полученный от BotFather.

5. Запустите бота:

   ```bash
   python main.py
   ```

## Команды

- `/start` - Начать игру
- `/quiz` - Начать квиз (можно запустить через кнопку "Начать игру")

## Ссылка на бота

[Ваш бот](https://t.me/kviz_please_bot)