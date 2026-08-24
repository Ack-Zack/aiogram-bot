from aiogram import Router, F, Bot
# можно определять на какие команды отвечать
from aiogram.filters import Command
# классы
from aiogram.types import Message, FSInputFile
from forms.user import Form  # можно заполнять форму
from aiogram.fsm.context import FSMContext  # позволяет запрашивать информацию у пользователя


# можно определять на что отвечать
router = Router()


@router.message(Command('start'))
async def start(message: Message, state: FSMContext):
    await message.answer('Давайте начнем заполнять анкету!\nСперва введите ваше имя:')
    await state.set_state(Form.name)


@router.message(Command('cancel'))
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Анкета отклонена!')


@router.message(Form.name, F.text)
async def process_name(message: Message, state: FSMContext):
    user_name = message.text.strip()
    await state.update_data(name=user_name)

    await message.answer('Отлично!\nА теперь введите ваш возраст:')
    await state.set_state(Form.age)


@router.message(Form.age, F.text)
async def process_age(message: Message, state: FSMContext):
    user_age = message.text.strip()
    if not user_age.isdigit():
        await message.answer('Возраст должен быть числом')
        return
    elif not 1 <= int(user_age) <= 100:
        await message.answer('Возраст должен быть от 1 до 100')
        return

    await state.update_data(age=int(user_age))

    await message.answer('Отлично!\nА теперь введите ваш email:')
    await state.set_state(Form.email)


@router.message(Form.email, F.text)
async def process_email(message: Message, state: FSMContext):
    user_email = message.text.strip()
    if '@' not in user_email or '.' not in user_email:
        await message.answer('Email не корректный')
        return

    await state.update_data(email=user_email)

    data = await state.get_data()
    name, age, email = data['name'], data['age'], data['email']

    await message.answer(f'Анкета готова!\nИмя: {name}\nВозраст: {age}\nПочта: {email}')
    await state.clear()  # выход из состояния


@router.message(F.photo)
async def process_photo(message: Message):
    photo = message.photo[-1]
    file_id = photo.file_id

    await message.answer(f'Вы отправили фото!\nID фото: - <code>{file_id}</code>',
                         parse_mode='HTML')

    await message.answer_photo(file_id, caption='Вот ваше фото')


@router.message(F.video)
async def process_video(message: Message):
    video = message.video
    file_id = video.file_id
    duration = video.duration

    await message.answer(
        f'Вы отправили видео!\nID видео: - <code>{file_id}</code> Длительность видео: - <code>{duration}</code> сек.',
        parse_mode='HTML')

    await message.answer_video(file_id, caption='Вот ваше видео')


@router.message(F.animation)
async def process_animation(message: Message):
    animation = message.animation
    file_id = animation.file_id

    await message.answer(
        f'Вы отправили анимацию!\nID анимация: - <code>{file_id}</code>',
        parse_mode='HTML')

    await message.answer_animation(file_id, caption='Вот ваша анимация')


@router.message(F.document)
async def process_animation(message: Message, bot: Bot):
    document = message.document
    file_id = document.file_id

    file = await bot.get_file(file_id)
    file_path = file.file_path

    local_path = f'downloads/{document.file_name}'
    await bot.download_file(file_path=file_path, destination=local_path)

    await message.answer('Файл сохранен!')


@router.message(Command('file'))
async def send_file(message: Message):
    file = FSInputFile('files/example.txt')

    await message.answer_document(file)








