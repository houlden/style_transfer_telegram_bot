import asyncio
import io
import multiprocessing
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

from bot_init import dp, bot
from ml_models.nst_gatys.run_style_transfer import run
from keyboards import standard, inline


class FSM_NST(StatesGroup):
    """
    Класс конечного автомата для диалога с пользователем и реализации style transfer.
    """
    get_style_image = State()
    get_content_image_save_data_and_processing = State()


async def start_nst(callback: CallbackQuery):
    """
    Запускает процесс style transfer.
    """
    await FSM_NST.first()  # Перевод программы в начальное состояние КА
    await callback.message.answer(
        'Загрузите изображение, стиль которого нужно перенести:'
        '\n(для выхода из процесса обработки нажмите "Cancel")',
        reply_markup=standard.user_kb.cancel_kb
    )
    await callback.answer()


async def cancel_nst(message: Message, state: FSMContext):
    """
    Выводит программу из текущего состояния в состояние None.
    """
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer('Обработка прервана, попробуем снова?', reply_markup=inline.user_kb.mode_selection_kb)


async def get_style_image(message: Message, state: FSMContext):
    """
    Получает изображение стиля от пользователя и помещает его ID в оперативную память.
    """
    async with state.proxy() as data:
        data['style'] = message.photo[-1].file_id  # [-1] - ID изображения в исходном разрешении
    await FSM_NST.next()
    await message.answer('Загрузите изображение, которое нужно стилизовать')


async def get_content_image_save_data_and_processing(message: Message, state: FSMContext):
    """
    Получает изображение контента от пользователя и помещает его ID в оперативную память.
    Запускает загрузку изображений style и content с серверов telegram и передает из в функцию image_processing для
    запуска стилизации.
    """
    async with state.proxy() as data:
        data['content'] = message.photo[-1].file_id
    style_image, content_image = await download_data(state=state)
    await image_processing(message=message, style_image=style_image, content_image=content_image)
    await message.answer('Добавлено в очередь на обработку. Стилизация производится на CPU, это займет некоторое время.'
                         '\nЧто-нибудь ещё?', reply_markup=inline.user_kb.mode_selection_kb)
    await state.finish()


async def download_data(state: FSMContext):
    """
    Загружает с серверов telegram по ID изображения style и content.
    :return downloaded_style: io.BytesIO, downloaded_content: io.BytesIO - изображения style и content.
    """
    async with state.proxy() as data:
        style_id = data['style']
        content_id = data['content']

    file_style = await bot.get_file(style_id)
    file_content = await bot.get_file(content_id)

    downloaded_style = await bot.download_file(file_style.file_path)
    downloaded_content = await bot.download_file(file_content.file_path)

    return downloaded_style, downloaded_content


async def image_processing(message: Message, style_image: io.BytesIO, content_image: io.BytesIO):
    """
    Асинхронно запускает функцию run в отдельном пуле процессов для переноса стиля.
    Перенесенный стиль отправляется пользователю через callback.
    :param message: Message
    :param style_image: io.BytesIO - изображение style
    :param content_image: io.BytesIO - изображение content
    """
    # Получим цикл обработки событий основного потока для того, чтобы из синхронного метода callback запустить
    # асинхронный метод bot.send_photo.
    loop = asyncio.get_event_loop()

    def send_output_image(output_image):
        """
        Отправляет пользователю перенесенный стиль по callback-у
        :param output_image: io.BytesIO - результат переноса стиля
        """
        loop.create_task(bot.send_photo(message.from_user.id, output_image))

    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    pool.apply_async(func=run, args=(style_image, content_image,), callback=send_output_image)


def register_handlers_nst(dp: Dispatcher):
    """
    Регистрирует все хэндлеры.
    """
    dp.register_callback_query_handler(start_nst, text='NST-Gatys', state=None)
    dp.register_message_handler(cancel_nst, Text(equals='Cancel', ignore_case=True), state='*')
    dp.register_message_handler(get_style_image, content_types=['photo'], state=FSM_NST.get_style_image)
    dp.register_message_handler(get_content_image_save_data_and_processing, content_types=['photo'],
                                state=FSM_NST.get_content_image_save_data_and_processing)


register_handlers_nst(dp)
