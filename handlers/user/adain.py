from aiogram.types import CallbackQuery

from bot_init import dp
from keyboards import inline


@dp.callback_query_handler(text='AdaIN', state=None)
async def start_nst(callback: CallbackQuery):
    await callback.message.answer('В разработке', reply_markup=inline.user_kb.mode_selection_kb)
    await callback.answer()