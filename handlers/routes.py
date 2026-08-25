from aiogram import Router
# можно определять на какие команды отвечать
from aiogram.filters import Command
# классы
from aiogram.types import Message
import aiosqlite


# можно определять на что отвечать
router = Router()


# ---

DB_NAME = 'first_aiosqlite.db'


async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT,
            age INTEGER
        );
        ''')
        await db.commit()


async def add_user(full_name, age):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
        INSERT INTO users (full_name, age)
        VALUES (?, ?)
        ''', (full_name, age))

        await db.commit()


async def get_users():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute('SELECT full_name, age FROM users;')
        result = await cursor.fetchall()
        return result

# ---


# отвечает только на команду /start
@router.message(Command('start'))
async def start(message: Message):
    await init_db()
    await message.answer('Привет!\nПропишите команду: /reg AGE')


@router.message(Command('reg'))
async def reg(message: Message):
    parts = message.text.strip().split()

    if len(parts) != 2 or not parts[1].isdigit():
        await message.answer('Ошибка: Неправильный формат')
        return

    await add_user(message.from_user.full_name, int(parts[1]))
    await message.answer('Готово!')


@router.message(Command('users'))
async def users(message: Message):
    users = await get_users()

    if not users:
        await message.answer('Ошибка: В базе нет пользователей')
        return

    text = 'Пользователи в базе:\n\n'
    for full_name, age in users:
        text += f'- {full_name} - <code>{age}</code>\n'

    await message.answer(text, parse_mode='HTML')


