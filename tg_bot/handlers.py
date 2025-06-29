from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from application.commands import create_item, create_storage
from application.database import get_session
from const import ITEM_IMG, STORAGE_IMG

router = Router()


class AddStorage(StatesGroup):
    waiting_for_name = State()
    waiting_for_photo = State()


class AddItem(StatesGroup):
    waiting_for_data = State()
    waiting_for_photo = State()


@router.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer(
        'Привет! Я помогаю хранить всё на своих местах.\n'
        'Чтобы добавить хранилище: /add_storage <название>\n'
        'Чтобы добавить предмет: /add_item <название> <имя_хранилища> [info]\n'
        'И пришли фото после команды.'
    )


@router.message(Command('add_storage'))
async def cmd_add_storage(message: Message, state: FSMContext):
    parts = message.text
    if len(parts) < 2 or parts is None:
        return await message.reply('Добавить хранилище: /add_storage <название>')

    parts = parts.split(maxsplit=1)
    name = parts[1].strip()

    await state.update_data(action='storage', name=name)
    await state.set_state(AddStorage.waiting_for_photo)
    await message.answer(f'Ок, пришлите фото для хранилища «{name}»')


@router.message(Command('add_item'))
async def cmd_add_item(message: Message, state: FSMContext):
    parts = message.text
    if len(parts) < 3 or parts is None:
        return await message.reply(
            'Добавить предмет в хранилище: /add_item <название> <имя_хранилища> [info]'
        )
    parts = parts.split(maxsplit=3)
    _, name, storage_name, *info = parts
    info = info[0] if info else None

    await state.update_data(action='item', name=name, storage_name=storage_name, info=info)
    await state.set_state(AddItem.waiting_for_photo)
    await message.answer(f'Пришлите фото для предмета "{name}" в хранилище "{storage_name}"')


@router.message(AddStorage.waiting_for_photo, F.photo)
async def process_storage_photo(message: Message, state: FSMContext):
    data = await state.get_data()
    name = data['name']

    photo = message.photo[-1]
    filename = f'storage_{message.from_user.id}_{photo.file_unique_id}.jpg'
    dest = STORAGE_IMG / filename
    file = await message.bot.get_file(photo.file_id)
    await message.bot.download_file(file.file_path, destination=dest)

    async for session in get_session():
        obj = await create_storage(session, name, str(dest))
    await message.answer(f'Создано хранилище: {obj.name}')
    await state.clear()


@router.message(AddItem.waiting_for_photo, F.photo)
async def process_item_photo(message: Message, state: FSMContext):
    data = await state.get_data()
    photo = message.photo[-1]
    img = ITEM_IMG / f'item_{message.from_user.id}_{photo.file_unique_id}.jpg'

    file = await message.bot.get_file(photo.file_id)
    await message.bot.download_file(file.file_path, destination=img)

    async for session in get_session():
        obj = await create_item(
            session, data['name'], str(img), data['storage_name'], data.get('info')
        )
    await message.answer(
        f'Добавлен предмет {obj.id}: {obj.name} в хранилище {data["storage_name"]}'
    )
    await state.clear()
