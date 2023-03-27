from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
menu_keyboard.add(KeyboardButton('Знайти розклад')).add(KeyboardButton('Мій розклад')).add(KeyboardButton('Обране'))
