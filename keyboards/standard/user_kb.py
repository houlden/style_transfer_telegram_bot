from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# help_button = KeyboardButton('/help')
# nst_gatys_button = KeyboardButton('/NST-Gatys')
# gan_button = KeyboardButton('/GAN')
#
# mode_selection_kb = ReplyKeyboardMarkup(resize_keyboard=True)
#
# mode_selection_kb.row(help_button)
# mode_selection_kb.row(nst_gatys_button, gan_button)

cancel_kb = ReplyKeyboardMarkup(resize_keyboard=True)
cancel_button = KeyboardButton('/cancel')
cancel_kb.row(cancel_button)
