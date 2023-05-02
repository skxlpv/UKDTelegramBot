from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.database.pref_requests import get_preferences
from bot.storage.placeholders import buttons


def get_settings_keyboard(user):
    settings_keyboard = InlineKeyboardMarkup(row_width=1)

    user_prefs = get_preferences(user)

    additional_param = 'Так' if user_prefs['additional_courses'] else 'Ні'
    morning_param = 'Так' if user_prefs['morning_schedule'] else 'Ні'
    additional_courses = InlineKeyboardButton(text=buttons.SHOW_ADDITIONAL_COURSES % additional_param,
                                              callback_data='additional_courses')
    morning_schedule = InlineKeyboardButton(text=buttons.SEND_MORNING_SCHEDULE % morning_param,
                                            callback_data='morning_schedule')

    return settings_keyboard.add(additional_courses).add(morning_schedule)
