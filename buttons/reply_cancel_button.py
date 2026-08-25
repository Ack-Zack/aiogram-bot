from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_cancel_reply_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Отмена')]
        ],
        resize_keyboard=True,
    )
    return keyboard

