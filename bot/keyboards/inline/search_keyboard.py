from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup

from bot.storage.placeholders import buttons

button_choice_search = InlineKeyboardButton(text=buttons.ROLE, callback_data='choice_search')
button_manual_search = InlineKeyboardButton(text=buttons.NAME, callback_data='manual_search')
search_keyboard = InlineKeyboardMarkup().add(button_choice_search, button_manual_search)
