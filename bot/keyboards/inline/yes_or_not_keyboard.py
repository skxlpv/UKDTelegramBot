from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup

from bot.storage.placeholders import buttons

yes = InlineKeyboardButton(text=buttons.YES, callback_data='yes')
no = InlineKeyboardButton(text=buttons.NO, callback_data='no')

tip_keyboard = InlineKeyboardMarkup().add(yes, no)
