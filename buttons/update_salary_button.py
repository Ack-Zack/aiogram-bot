from aiogram import Router, F
from aiogram.fsm.context import FSMContext

from Forms.user import PayWages
from buttons.reply_cancel_button import get_cancel_reply_keyboard
from handlers.users_data_base import update_salary_db, is_not_in


from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove


router = Router()


@router.callback_query(lambda c: c.data == 'update_salary')
async def update_salary_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Начинаем обновлять зарплату работнику!\nДля начала введите имя работника:',
                                  reply_markup=get_cancel_reply_keyboard())

    await state.set_state(PayWages.name)
    await callback.answer()


@router.message(PayWages.name, F.text)
async def process_name(message: Message, state: FSMContext):
    user_name = message.text.strip().title()
    if await is_not_in(user_name):
        await message.answer(f'Ошибка: Имя - {user_name} не зарегистрировано!\nПопробуйте еще раз:')
        return

    await state.update_data(name=user_name)

    await message.answer('Отлично!\nДальше введите новую зарплату для этого сотрудника:')

    await state.set_state(PayWages.salary)


@router.message(PayWages.salary, F.text)
async def process_salary(message: Message, state: FSMContext):
    new_salary = message.text.strip()
    if not new_salary.isdigit():
        await message.answer('Ошибка: Зарплата должна быть числом\n Попробуйте еще раз:')
        return

    await state.update_data(salary=new_salary)

    data = await state.get_data()
    name = data['name']
    new_salary = data['salary']
    await update_salary_db(name, new_salary)

    await message.answer('Зарплата обновлена успешно!',
                         reply_markup=ReplyKeyboardRemove())

    await state.clear()


