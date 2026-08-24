from aiogram import Router
# можно определять на какие команды отвечать
from aiogram.filters import Command
# классы
from aiogram.types import Message, BufferedInputFile
import aiohttp

# можно определять на что отвечать
router = Router()


# получить информацию о продукте по id
async def get_product(product_id):
    url = f'https://fakestoreapi.com/products/{product_id}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data
            return None


# отправить информацию о продукте в чат
async def send_info(message: Message, image_url, text):
    async with aiohttp.ClientSession() as session:
        async with session.get(image_url) as response:
            if response.status == 200:
                image_bytes = await response.read()

                photo = BufferedInputFile(image_bytes, filename="image.jpg")

                await message.answer_photo(photo=photo, caption=f'{text}', parse_mode='HTML')
            else:
                await message.answer("Не удалось скачать картинку.")


async def get_product_id(message: Message):
    parts = message.text.strip().split()
    product_id = parts[1]
    if len(parts) != 2:
        await message.answer(
            'Ошибка: Неверный формат\n\nПример: <b>product 1</b>',
            parse_mode='HTML'
        )
        return None

    product_id = parts[1]
    if not product_id.isdigit():
        await message.answer('Ошибка: ID товара должен быть числом')
        return None
    return product_id


# отвечает только на команду /start
@router.message(Command('start'))
async def start(message: Message):
    await message.answer(
        'Привет! Я простой бот-магазин.\nВведите команду: /product ID\n\nПример: <b>/product 1</b>',
        parse_mode='HTML'
    )


@router.message(Command('product'))
async def get_product_cmd(message: Message):
    product_id = await get_product_id(message)
    if product_id is None:
        return
    await message.answer(f'ищу товар с ID: {product_id}')

    try:
        product = await get_product(int(product_id))
    except Exception:
        await message.answer('Ошибка: Не удалось обратиться к серверу')
        return

    if product is None:
        await message.answer(f'Ошибка: Товара с ID: {product_id} нет')
        return

    title = product.get('title', '-')
    price = product.get('price', '-')
    desc = product.get('description', '-')
    category = product.get('category', '-')
    image = product.get('image')

    text = (
        f'<b>{title}</b>\n\n'
        f'Категория: <i>{category}</i>\n'
        f'Цена: <i>{price}</i>\n'
        f'{desc}'
    )
    try:
        await send_info(message, image, text)
    except Exception:
        await message.answer('Ошибка: Не удалось обратиться к серверу')


