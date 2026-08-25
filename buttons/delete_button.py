from aiogram import Router, F
from aiogram.fsm.context import FSMContext

from Forms.user import Name
from handlers.users_data_base import delete_worker_from_db, is_not_in
from buttons.reply_cancel_button import get_cancel_reply_keyboard
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

router = Router()


@router.callback_query(lambda c: c.data == 'delete_worker')
async def delete_worker(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Начинаем удалять сотрудника\nНапишите имя работника:',
                                  reply_markup=get_cancel_reply_keyboard())
    await state.set_state(Name.name)
    await callback.answer()


@router.message(Name.name, F.text)
async def process_delete_name(message: Message, state: FSMContext):
    user_name = message.text.strip().title()

    if await is_not_in(user_name):
        await message.answer(f'Ошибка: Имя - {user_name} не зарегистрировано!\nПопробуйте еще раз:')
        return

    await state.update_data(name=user_name)

    data = await state.get_data()
    name = data['name'].strip().title()
    try:
        await delete_worker_from_db(name)
    except ValueError:
        await message.answer(f'Работника с именем "{name}" не существует\nПопробуйте еще раз:')
        return
    else:
        await message.answer('Работник успешно удален!',
                             reply_markup=ReplyKeyboardRemove())
        await state.clear()