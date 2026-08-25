import aiosqlite
from datetime import datetime

DB_NAME = 'Workers.db'


async def create_table():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        salary INTEGER NOT NULL,
        bill INTEGER NOT NULL,
        date TEXT NOT NULL,
        graphic TEXT DEFAULT 0
    );''')
    await db.commit()


async def get_salary():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute('SELECT name, salary, bill FROM Users;')
        result = await cursor.fetchall()
        return result


async def add_worker_to_db(name, salary, bill, graphic):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
        INSERT INTO Users (name, salary, bill, date, graphic) VALUES (?, ?, ?, ?, ?)
        ''', (name, salary, bill, datetime.now().strftime('%d-%m-%Y'), graphic))

        await db.commit()


async def delete_worker_from_db(name):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute('''
        SELECT name
        FROM Users
        WHERE name = ?;
        ''', (name,))

        row = await cursor.fetchone()

        if row is None:
            raise ValueError('такого имени в базе данных нет')

        await cursor.execute('''
        DELETE FROM Users
        WHERE name = ?;
        ''', (name,))

        await db.commit()


async def pay_wages_db(name, bill, flag):
    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute('''
        SELECT name
        FROM Users
        WHERE name = ?;
        ''', (name,))

        row = await cursor.fetchone()

        if row is None:
            raise ValueError('такого имени в базе данных нет')
        if flag:
            await cursor.execute('''
            UPDATE Users
            SET bill = 0
            WHERE name = ?;
            ''', (name,))
        else:
            await cursor.execute('''
            UPDATE Users
            SET bill = bill - ?
            WHERE name = ?;
            ''', (bill, name))

        await db.commit()


async def statistics_db():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute('''
        SELECT name, salary, bill, date
        FROM Users;''')

        info = await cursor.fetchall()
        if not info:
            raise ValueError('База данных пуста')
        res = 0
        workers = {}
        for name, salary, bill, iso_date in info:
            res += bill
            workers[name] = name, salary, bill, iso_date
        return workers, res


async def update_salary_db(name, salary):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
        UPDATE Users
        SET salary = ?
        WHERE name = ?;
        ''', (salary, name))


async def is_not_in(user_name):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute('''
        SELECT name 
        FROM Users
        WHERE name = ?;
        ''', (user_name,))

        user_name_list = await cursor.fetchone()

        result = user_name_list is None
        return result
