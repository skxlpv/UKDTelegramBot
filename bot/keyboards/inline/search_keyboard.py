from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup


button_choice_search = InlineKeyboardButton(text='За критеріями', callback_data='choiceSearch')
button_manual_search = InlineKeyboardButton(text='За назвою', callback_data='manualSearch')
search_keyboard = InlineKeyboardMarkup().add(button_choice_search, button_manual_search)