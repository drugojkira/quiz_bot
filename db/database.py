import aiosqlite

DB_NAME = 'quiz_bot.db'


async def create_table():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state (
            user_id INTEGER PRIMARY KEY,
            question_index INTEGER
        )''')
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_results (
            user_id INTEGER,
            score INTEGER,
            correct_answers INTEGER,
            incorrect_answers INTEGER
        )''')  # Обновленная таблица
        await db.execute('''CREATE TABLE IF NOT EXISTS asked_questions (
            user_id INTEGER,
            question_index INTEGER
        )''')
        await db.commit()


async def get_quiz_index(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            'SELECT question_index FROM quiz_state WHERE user_id = ?',
            (user_id,)
        ) as cursor:
            results = await cursor.fetchone()
            return results[0] if results else 0


async def update_quiz_index(user_id, index):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            'INSERT OR REPLACE INTO quiz_state (user_id, question_index) VALUES (?, ?)',
            (user_id, index)
        )
        await db.commit()


async def save_quiz_result(user_id, score, correct_answers, incorrect_answers):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            'INSERT INTO quiz_results (user_id, score, correct_answers, incorrect_answers) VALUES (?, ?, ?, ?)',
            (user_id, score, correct_answers, incorrect_answers)
        )
        await db.commit()
