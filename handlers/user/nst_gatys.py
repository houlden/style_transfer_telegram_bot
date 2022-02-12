import asyncio
import os
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
import multiprocessing

from bot_init import dp, bot
from ml_models.nst_gatys.run_style_transfer import run
from keyboards import standard, inline


class FSM_NST(StatesGroup):
    get_style_image = State()
    get_content_image_save_data_and_processing = State()


async def start_nst(callback: CallbackQuery):
    await callback.message.answer(
        'Загрузите изображение, стиль которого нужно перенести'
    )
    await FSM_NST.first()
    await callback.message.answer('Для выхода из процесса обработки нажмите "Cancel"',
                                  reply_markup=standard.user_kb.cancel_kb)
    await callback.answer()


# async def cancel_nst(callback: CallbackQuery, state: FSMContext):
#     await state.finish()
#     await callback.message.answer('Обработка прервана, попробуем снова?', reply_markup=user_kb.mode_selection_kb)
#     await callback.answer()


async def cancel_nst(message: Message, state: FSMContext):
    # async with state.proxy() as data:
    #     print(data.state)
    await state.finish()
    await message.answer('Обработка прервана, попробуем снова?', reply_markup=inline.user_kb.mode_selection_kb)


async def get_style_image(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['style'] = message.photo[-1].file_id
    await FSM_NST.next()
    await message.answer('Загрузите изображение, которое нужно стилизовать')
    # await message.answer('Для выхода из процесса обработки нажмите "Cancel"', reply_markup=standard.user_kb.cancel_kb)


async def get_content_image_save_data_and_processing(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['content'] = message.photo[-1].file_id
    await message.answer('Обработка может занять около 10 минут, вычисления производятся на CPU')
    # await message.answer('Для выхода из процесса обработки нажмите "Cancel"', reply_markup=standard.user_kb.cancel_kb)
    style_path, content_path, output_path = await save_data(state=state)
    await image_processing(message=message, style_path=style_path, content_path=content_path, output_path=output_path)
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
    # dp.register_callback_query_handler(cancel_nst, text='cancel', state='*')
    dp.register_message_handler(cancel_nst, commands=['cancel'], state='*')
    dp.register_message_handler(get_style_image, content_types=['photo'], state=FSM_NST.get_style_image)
    dp.register_message_handler(get_content_image_save_data_and_processing, content_types=['photo'],
                                state=FSM_NST.get_content_image_save_data_and_processing)


register_handlers_nst(dp)
