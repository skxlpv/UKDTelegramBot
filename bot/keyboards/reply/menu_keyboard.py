from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.storage.placeholders import buttons

menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
menu_keyboard.add(KeyboardButton(buttons.FIND_SCHEDULE)).add(KeyboardButton(buttons.MY_SCHEDULE)).add(KeyboardButton(buttons.FAVORITES))
