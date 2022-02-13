from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# Основная клавиатура - выбор режима работы
mode_selection_kb = InlineKeyboardMarkup(row_width=1)

help_button = InlineKeyboardButton('Help', callback_data='help')
nst_gatys_button = InlineKeyboardButton('NST-Gatys', callback_data='NST-Gatys')
adain_button = InlineKeyboardButton('AdaIN', callback_data='AdaIN')

mode_selection_kb.row(help_button)
mode_selection_kb.row(nst_gatys_button, adain_button)
