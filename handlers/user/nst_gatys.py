import asyncio
import multiprocessing
import os
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

from bot_init import dp, bot
from ml_models.nst_gatys.run_style_transfer import run
from keyboards import standard, inline


class FSM_NST(StatesGroup):
    get_style_image = State()
    get_content_image_save_data_and_processing = State()


async def start_nst(callback: CallbackQuery):
    await FSM_NST.first()
    await callback.message.answer(
        'Загрузите изображение, стиль которого нужно перенести:'
        '\n(для выхода из процесса обработки нажмите "Cancel")',
        reply_markup=standard.user_kb.cancel_kb
    )
    await callback.answer()


async def cancel_nst(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer('Обработка прервана, попробуем снова?', reply_markup=inline.user_kb.mode_selection_kb)


async def get_style_image(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['style'] = message.photo[-1].file_id
    await FSM_NST.next()
    await message.answer('Загрузите изображение, которое нужно стилизовать')


async def get_content_image_save_data_and_processing(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['content'] = message.photo[-1].file_id
    style_path, content_path, output_path = await save_data(state=state)
    await image_processing(message=message, style_path=style_path, content_path=content_path, output_path=output_path)
    await message.answer('Добавлено в очередь на обработку. Стилизация производится на CPU, это займет некоторое время.'
                         '\nЧто-нибудь ещё?', reply_markup=inline.user_kb.mode_selection_kb)
    await state.finish()


async def save_data(state: FSMContext):
    async with state.proxy() as data:
        style_id = data['style']
        content_id = data['content']

    file_style = await bot.get_file(style_id)
    file_content = await bot.get_file(content_id)

    downloaded_style = await bot.download_file(file_style.file_path)
    downloaded_content = await bot.download_file(file_content.file_path)

    _, style_extension = os.path.splitext(file_style.file_path)
    _, content_extension = os.path.splitext(file_content.file_path)

    style_path = 'images/' + style_id + style_extension
    content_path = 'images/' + content_id + content_extension
    output_path = 'images/' + style_id + content_id + content_extension

    with open(style_path, 'wb') as f:
        f.write(downloaded_style.read())

    with open(content_path, 'wb') as f:
        f.write(downloaded_content.read())

    return style_path, content_path, output_path


async def image_processing(message: Message, style_path, content_path, output_path):
    loop = asyncio.get_event_loop()

    def send_output_image(output_image):
        loop.create_task(bot.send_photo(message.from_user.id, output_image))

    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    pool.apply_async(func=run, args=(style_path, content_path, output_path,), callback=send_output_image)


def register_handlers_nst(dp: Dispatcher):
    dp.register_callback_query_handler(start_nst, text='NST-Gatys', state=None)
    dp.register_message_handler(cancel_nst, Text(equals='Cancel', ignore_case=True), state='*')
    dp.register_message_handler(get_style_image, content_types=['photo'], state=FSM_NST.get_style_image)
    dp.register_message_handler(get_content_image_save_data_and_processing, content_types=['photo'],
                                state=FSM_NST.get_content_image_save_data_and_processing)


register_handlers_nst(dp)
