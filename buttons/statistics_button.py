from aiogram import Router

from handlers.users_data_base import statistics_db

from aiogram.types import CallbackQuery


router = Router()


@router.callback_query(lambda c: c.data == 'statistics')
async def statistics(callback: CallbackQuery):
    try:
        workers, rub = await statistics_db()
    except ValueError as e:
        await callback.message.answer(str(e))
        return
    else:
        result = '\n'.join(f'{name}: Зарплата - {salary}\nСчет - {bill}\nДата регистрации - {string_date}' for name, salary, bill, string_date in workers.values())

        await callback.message.answer(f'{result}\nОбщая задолженность: {rub} Рублей')
        await callback.answer()
