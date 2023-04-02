from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup

yes = InlineKeyboardButton(text='Так', callback_data='yes')
no = InlineKeyboardButton(text='Ні', callback_data='no')

tip_keyboard = InlineKeyboardMarkup().add(yes, no)
