from aiogram import Router, F
from aiogram.fsm.context import FSMContext

from Forms.user import PayWages
from handlers.users_data_base import pay_wages_db, is_not_in
from buttons.reply_cancel_button import get_cancel_reply_keyboard

from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove


router = Router()


@router.callback_query(lambda c: c.data == 'pay_wages')
async def pay_wages(callback: CallbackQuery, state):
    await callback.message.answer('Начинаем выплату\nНапишите имя работника:',
                                  reply_markup=get_cancel_reply_keyboard())

    await state.set_state(PayWages.name)
    await callback.answer()


@router.message(PayWages.name, F.text)
async def process_pay_wages_name(message: Message, state: FSMContext):
    user_name = message.text.strip().title()

    if await is_not_in(user_name):
        await message.answer(f'Ошибка: Имя - {user_name} не зарегистрировано!\nПопробуйте еще раз:')
        return

    await state.update_data(name=user_name)

    await message.answer(
        'Имя установлено!\nА теперь введите сколько вы хотите выплатить (или напишите "-1" для выдачи всей зарплаты):')
    await state.set_state(PayWages.salary)


@router.message(PayWages.salary, F.text)
async def process_pay_wages_salary(message: Message, state: FSMContext):
    bill = message.text.strip()
    flag = bill.lower() == '-1'
    if not flag:
        if not bill.isdigit():
            await message.answer(f'Зарплата должна быть числом\nПопробуйте еще раз:')
            return
        elif int(bill) < 0:
            await message.answer(f'Нельзя выдать зарплату меньше нуля! попробуйте еще раз:')
            return
    await state.update_data(salary=int(bill))

    data = await state.get_data()
    name, bill = data['name'], data['salary']

    try:
        await pay_wages_db(name, bill, flag)
    except ValueError as e:
        await message.answer(str(e))
        return
    else:
        await message.answer('Зарплата выдана успешно!',
                             reply_markup=ReplyKeyboardRemove())
    await state.clear()