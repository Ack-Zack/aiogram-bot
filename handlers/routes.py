from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from buttons.salary_button import router as salary_router
from buttons.add_worker_button import router as add_worker_router
from buttons.delete_button import router as delete_worker_router
from buttons.update_salary_button import router as new_salary_router
from buttons.pay_wages_button import router as pay_wages_router
from buttons.statistics_button import router as statistics_router

from buttons.inline_buttons import get_main_inline_keyboard
from handlers.users_data_base import create_table

from aiogram.types import Message, ReplyKeyboardRemove


router = Router()
#  ДОБАВИТЬ РАБОТНИКА
router.include_router(add_worker_router)
# ЗАРПЛАТЫ
router.include_router(salary_router)
# УДАЛИТЬ
router.include_router(delete_worker_router)
# ОБНОВИТЬ
router.include_router(new_salary_router)
# ВЫПЛАТА
router.include_router(pay_wages_router)
#  СТАТИСТИКА
router.include_router(statistics_router)


#  СТАРТ
@router.message(Command('start'))  # отвечает только на команду /start
@router.message(F.text.lower() == 'старт')  # отвечает на строку старт
async def start(message: Message):
    await message.answer('Привет! я простой бот для тебя',
                         reply_markup=get_main_inline_keyboard())
    await create_table()


# ОТМЕНА
@router.message(Command("cancel"))
@router.message(F.text.casefold() == "отмена")
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Действие отменено", reply_markup=ReplyKeyboardRemove())

