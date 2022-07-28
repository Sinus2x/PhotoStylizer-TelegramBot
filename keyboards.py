from aiogram import types

kb = types.InlineKeyboardMarkup(row_width=2)
kb.row(types.InlineKeyboardButton(text='Ок', callback_data='yes'),
       types.InlineKeyboardButton(text='Поменять фото', callback_data='change'))