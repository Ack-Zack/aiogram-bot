from aiogram import Router
from handlers.users_data_base import get_salary

from aiogram.types import CallbackQuery
router = Router()


@router.callback_query(lambda c: c.data == 'salary')
async def salary(callback: CallbackQuery):
    result = await get_salary()
    if not result:
        await callback.message.answer('Пусто')
        return
    text = ''
    for name, salary, bill in result:
        text += f'\nИмя: {name}, Зарплата: {salary}, Счет: {bill}'
    await callback.message.answer(text)
    await callback.answer()