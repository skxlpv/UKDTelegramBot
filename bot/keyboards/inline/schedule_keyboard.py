from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

schedule_keyboard = InlineKeyboardMarkup(row_width=3)

mn = InlineKeyboardButton(text="Пн", callback_data='mn')
ts = InlineKeyboardButton(text="ВТ", callback_data='ts')
wd = InlineKeyboardButton(text="Ср", callback_data='wd')
th = InlineKeyboardButton(text="Чт", callback_data='th')
we = InlineKeyboardButton(text="Пт", callback_data='we')
week = InlineKeyboardButton(text="Роклад на тиждень", callback_data='Week')
next = InlineKeyboardButton(text="Наступний тиждень", callback_data='Next')

schedule_keyboard.row(mn, ts, wd, th, we).add(week, next)