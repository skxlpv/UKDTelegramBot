from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup


button_choice_search = InlineKeyboardButton(text='За роллю', callback_data='choice_search')
button_manual_search = InlineKeyboardButton(text='За назвою', callback_data='manual_search')
search_keyboard = InlineKeyboardMarkup().add(button_choice_search, button_manual_search)
