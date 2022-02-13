from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


cancel_kb = ReplyKeyboardMarkup(resize_keyboard=True)
cancel_button = KeyboardButton('Cancel')
cancel_kb.row(cancel_button)
