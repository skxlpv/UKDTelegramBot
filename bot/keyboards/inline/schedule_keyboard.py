from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.database.schedule_requests import get_one_if_exist

mn = InlineKeyboardButton(text="Пн", callback_data='mn')
ts = InlineKeyboardButton(text="Вт", callback_data='ts')
wd = InlineKeyboardButton(text="Ср", callback_data='wd')
th = InlineKeyboardButton(text="Чт", callback_data='th')
fr = InlineKeyboardButton(text="Пт", callback_data='fr')
week = InlineKeyboardButton(text="Тиждень", callback_data='week')
next_week = InlineKeyboardButton(text="Наступний тиждень", callback_data='next_week')
menu = InlineKeyboardButton(text='Меню', callback_data='menu')


def get_schedule_keyboard(user, group_id, isTeacher):
    schedule_keyboard = InlineKeyboardMarkup(row_width=3)
    isFavorite = get_one_if_exist(user=user, group_id=group_id, isTeacher=isTeacher, action='favorites')
    isPrimary = get_one_if_exist(user=user, group_id=group_id, isTeacher=isTeacher, action='primary')
    if not isPrimary:
        primary = InlineKeyboardButton(text='Позначити основним', callback_data='primary')
    else:
        primary = InlineKeyboardButton(text='Видалити з основного', callback_data='primary')
    if not isFavorite:
        favorite = InlineKeyboardButton(text='Додати до обраного', callback_data='favorite')
    else:
        favorite = InlineKeyboardButton(text='Видалити з обраного', callback_data='favorite')
    return schedule_keyboard.row(mn, ts, wd, th, fr).add(week, next_week).add(primary, favorite).add(menu)
