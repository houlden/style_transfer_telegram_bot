from aiogram.types import Message, CallbackQuery
from keyboards.inline import user_kb
from bot_init import dp


@dp.message_handler(commands=['start'])
async def start_info(message: Message):
    """
    Отправляет пользователю инструкцию по использованию бота.
    """
    await message.answer(
        'Немного магии вне Хогвартса?\n'
        'Help - Возможности бота\n'
        'NST-Gatys - Neural Style Transfer (Gatys Algorithm)',
        reply_markup=user_kb.mode_selection_kb
    )


@dp.callback_query_handler(text='help')
async def help_info(callback: CallbackQuery):
    """
    Отправляет пользователю инструкцию по использованию бота.
    """
    await callback.message.answer(
        'Немного магии вне Хогвартса?\n'
        'Help - Возможности бота\n'
        'NST-Gatys - Neural Style Transfer (Gatys Algorithm)',
        reply_markup=user_kb.mode_selection_kb
    )
    await callback.answer()
