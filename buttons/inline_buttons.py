from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_main_inline_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Зарплаты', callback_data='salary')],
            [InlineKeyboardButton(text='Добавить', callback_data='add_worker')],
            [InlineKeyboardButton(text='Удалить', callback_data='delete_worker')],
            [InlineKeyboardButton(text='Изменить зарплату', callback_data='update_salary')],
            [InlineKeyboardButton(text='Выплата', callback_data='pay_wages')],
            [InlineKeyboardButton(text='Статистика', callback_data='statistics')]
        ]
    )
    return keyboard