from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


mode_selection_kb = InlineKeyboardMarkup(row_width=1)

help_button = InlineKeyboardButton('Help', callback_data='help')
nst_gatys_button = InlineKeyboardButton('NST-Gatys', callback_data='NST-Gatys')
gan_button = InlineKeyboardButton('GAN', callback_data='GAN')

mode_selection_kb.row(help_button)
mode_selection_kb.row(nst_gatys_button, gan_button)

# cancel_kb = InlineKeyboardMarkup(row_width=1)
# cancel_button = InlineKeyboardButton('Cancel', callback_data='cancel')
# cancel_kb.row(cancel_button)
