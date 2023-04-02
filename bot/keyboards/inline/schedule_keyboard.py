from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

schedule_keyboard = InlineKeyboardMarkup(row_width=3)

mn = InlineKeyboardButton(text="Пн", callback_data='mn')
ts = InlineKeyboardButton(text="ВТ", callback_data='ts')
wd = InlineKeyboardButton(text="Ср", callback_data='wd')
th = InlineKeyboardButton(text="Чт", callback_data='th')
fr = InlineKeyboardButton(text="Пт", callback_data='fr')
week = InlineKeyboardButton(text="Роклад на тиждень", callback_data='Week')
next_week = InlineKeyboardButton(text="Наступний тиждень", callback_data='Next')
general_schedule = InlineKeyboardButton(text='Позначити розклад основним', callback_data='general_schedule')
favorite = InlineKeyboardButton(text='Обране', callback_data='favorite')
menu = InlineKeyboardButton(text='Меню', callback_data='menu')

schedule_keyboard.row(mn, ts, wd, th, fr).add(week, next_week).add(general_schedule, favorite).add(menu)
