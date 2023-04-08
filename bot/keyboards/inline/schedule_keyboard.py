from datetime import datetime

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.database.schedule_requests import get_one_if_exist
from bot.storage.placeholders import buttons

week = InlineKeyboardButton(text=buttons.WEEK, callback_data='week')
next_week = InlineKeyboardButton(text=buttons.NEXT_WEEK, callback_data='next_week')


def get_schedule_keyboard(user, group_id, isTeacher, weekday=datetime.now().weekday()):
    schedule_keyboard = InlineKeyboardMarkup(row_width=3)

    mn = InlineKeyboardButton(text=buttons.MONDAY, callback_data='mn')
    ts = InlineKeyboardButton(text=buttons.TUESDAY, callback_data='ts')
    wd = InlineKeyboardButton(text=buttons.WEDNESDAY, callback_data='wd')
    th = InlineKeyboardButton(text=buttons.THURSDAY, callback_data='th')
    fr = InlineKeyboardButton(text=buttons.FRIDAY, callback_data='fr')
    emoji = buttons.EMOJI
    match weekday:
        case 0:
            mn = InlineKeyboardButton(text=emoji, callback_data='mn')
        case 1:
            ts = InlineKeyboardButton(text=emoji, callback_data='ts')
        case 2:
            wd = InlineKeyboardButton(text=emoji, callback_data='wd')
        case 3:
            th = InlineKeyboardButton(text=emoji, callback_data='th')
        case 4:
            fr = InlineKeyboardButton(text=emoji, callback_data='fr')
        case _:
            pass

    isFavorite = get_one_if_exist(user=user, group_id=group_id, isTeacher=isTeacher, action='favorites')
    isPrimary = get_one_if_exist(user=user, group_id=group_id, isTeacher=isTeacher, action='primary')

    if not isPrimary:
        primary = InlineKeyboardButton(text=buttons.PRIMARY_PICK, callback_data='primary')
    else:
        primary = InlineKeyboardButton(text=buttons.PRIMARY_UNPICK, callback_data='primary')
    if not isFavorite:
        favorite = InlineKeyboardButton(text=buttons.FAVORITE_PICK, callback_data='favorite')
    else:
        favorite = InlineKeyboardButton(text=buttons.FAVORITE_UNPICK, callback_data='favorite')
    return schedule_keyboard.row(mn, ts, wd, th, fr).add(week, next_week).add(primary, favorite)
