from aiogram.types import CallbackQuery

from bot_init import dp
from keyboards import inline


@dp.callback_query_handler(text='AdaIN', state=None)
async def start_nst(callback: CallbackQuery):
    """
    Заглушка до добавления модели AdaIN боту.
    """
    await callback.message.answer('Функциональность в разработке, а пока можно воспользоваться алгоритмом Гатиса',
                                  reply_markup=inline.user_kb.mode_selection_kb)
    await callback.answer()
