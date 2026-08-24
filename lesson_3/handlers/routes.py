from aiogram import Router, F
# можно определять на какие команды отвечать
from aiogram.filters import Command
# классы
from aiogram.types import (
    Message, CallbackQuery,
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)


# можно определять на что отвечать
router = Router()


# кнопки внизу чата
def get_main_reply_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='О боте')],
            [KeyboardButton(text='Старт'), KeyboardButton(text='Помощь')]
        ],
        resize_keyboard=True
    )

    return keyboard


# кнопки в чате
def get_main_inline_keyboard():  # кнопки
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Открыть сайт', url='https://google.com')],
            [InlineKeyboardButton(text='Подробнее', callback_data='more_info')]
        ]
    )

    return keyboard


# перехватывает callback_data
@router.callback_query(lambda c: c.data == 'more_info')  # запускать функцию при more_info
async def process_more_info(callback: CallbackQuery):
    await callback.message.answer('Вот более подробная информация')
    await callback.answer()  # закрыть общение


@router.message(Command('start'))  # отвечает только на команду /start
@router.message(F.text.lower() == 'старт')  # отвечает на строку старт
async def start(message: Message):
    await message.answer('Привет! я простой бот для тебя\n\nНапиши /help для помощи')


@router.message(Command('help'))  # отвечает только на команду /help
@router.message(F.text.lower() == 'помощь')  # отвечает на строку помощь
async def _help(message: Message):
    await message.answer(
        '''Команды: 
        /start - запустить бот
        /help - список команд
        /about - про нас''',
        reply_markup=get_main_reply_keyboard())


@router.message(Command('about'))  # отвечает только на команду /about
@router.message(F.text.lower() == 'о боте')  # отвечает на строку о боте
async def about(message: Message):
    await message.answer(f'это команда про бота. твое имя: {message.from_user.first_name}',
                         reply_markup=get_main_inline_keyboard())


# отвечает на все от пользователя
@router.message()
async def about(message: Message):
    await message.answer('Text message')




