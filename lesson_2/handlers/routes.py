from aiogram import Router
# можно определять на какие команды отвечать
from aiogram.filters import Command
# классы
from aiogram.types import Message


# можно определять на что отвечать
router = Router()


# отвечает только на команду /start
@router.message(Command('start'))
async def start(message: Message):
    await message.answer('Привет! я *простой* бот _для_ тебя\n\nНапиши /help для помощи',
                         parse_mode='MARKDOWN')


# отвечает только на команду /help
@router.message(Command('help'))
async def help(message: Message):
    await message.answer('Команды: \n<b>/start</b> - запустить бот\n<i>/help</i> - <a href="https://google.com">список команд</a>\n/about - про нас',
                         parse_mode='HTML')


# отвечает только на команду /about
@router.message(Command('about'))
async def about(message: Message):
    await message.answer(f'это команда про бота. твое имя: {message.from_user.first_name}')


# отвечает на все от пользователя
@router.message()
async def about(message: Message):
    await message.answer('Text message')




