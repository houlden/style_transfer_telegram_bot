from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# Клавиатура для выхода из состояния FSM
cancel_kb = ReplyKeyboardMarkup(resize_keyboard=True)
cancel_button = KeyboardButton('Cancel')
cancel_kb.row(cancel_button)
