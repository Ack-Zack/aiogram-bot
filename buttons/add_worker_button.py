from aiogram import Router, F
from aiogram.fsm.context import FSMContext

from Forms.user import Form
from buttons.reply_cancel_button import get_cancel_reply_keyboard
from handlers.users_data_base import add_worker_to_db, is_not_in


from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove


router = Router()


@router.callback_query(lambda c: c.data == 'add_worker')
async def add_worker(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Начинаем добавлять сотрудника\nНапишите имя работника:',
                                  reply_markup=get_cancel_reply_keyboard())
    await state.set_state(Form.name)
    await callback.answer()


@router.message(Form.name, F.text)
async def process_name(message: Message, state: FSMContext):
    user_name = message.text.strip().title()

    if not await is_not_in(user_name):
        await message.answer(f'Ошибка: Работник с именем - {user_name} уже зарегистрирован!\nПопробуйте еще раз:')
        return

    await state.update_data(name=user_name)

    await message.answer('Имя установлено!\nА теперь введите дневную зарплату сотрудника:')
    await state.set_state(Form.salary)


@router.message(Form.salary, F.text)
async def process_salary(message: Message, state: FSMContext):
    user_salary = message.text.strip()
    if not user_salary.isdigit():
        await message.answer('Зарплата должна быть числом!\nПопробуйте еще раз:')
        return
    await state.update_data(salary=int(user_salary))

    await message.answer('Отлично!\nНапишите рабочие дни :\nПонедельник - 1./Воскресенье - 7\n'
                         '(например: 1234567)')
    await state.set_state(Form.graphic)


@router.message(Form.graphic, F.text)
async def process_set_graphic(message: Message, state: FSMContext):
    graphic = message.text.strip()
    days = {
        '1': "Понедельник",
        '2': 'Вторник',
        '3': 'Среда',
        '4': 'Четверг',
        '5': 'Пятница',
        '6': 'Суббота',
        '7': 'Воскресенье',
    }
    result = '\n'.join(days[k] for k in graphic)
    await state.update_data(graphic='\n' + result)

    await message.answer('Отлично. График установлен!\nА теперь введите изначальный счет сотрудника (например - 0):')
    await state.set_state(Form.bill)


@router.message(Form.bill, F.text)
async def process_bill(message: Message, state: FSMContext):
    user_bill = message.text.strip()
    if not user_bill.isdigit():
        await message.answer('Счет должен быть числом!\nПопробуйте еще раз:')
        return
    await state.update_data(bill=int(user_bill))

    data = await state.get_data()
    name, salary, bill, graphic = data['name'], data['salary'], data['bill'], data['graphic']
    await add_worker_to_db(name, salary, bill, graphic)

    await message.answer(
        f'Работник добавлен успешно!\nИмя: {name}\nЗарплата: {salary}\nСчет: {bill} \nГрафик: {graphic}',
                         reply_markup=ReplyKeyboardRemove())
    await state.clear()
