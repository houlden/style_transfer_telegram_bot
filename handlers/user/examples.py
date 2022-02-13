from aiogram.types import CallbackQuery

from keyboards.inline import user_kb
from bot_init import dp, bot
from config import EXAMPLE_PATH_GATYS


@dp.callback_query_handler(text='example')
async def send_example(callback: CallbackQuery):
    """
    Отправляет примеры работы бота.
    """
    try:
        with open(EXAMPLE_PATH_GATYS, 'rb') as image:
            await bot.send_photo(callback.from_user.id, image, caption='Пример переноса стиля с помощью NST-Gatys')
            await callback.message.answer('Понравилось? Уверен, у тебя получится еще лучше!',
                                          reply_markup=user_kb.mode_selection_kb)
    except IOError:
        raise IOError

    await callback.answer()
