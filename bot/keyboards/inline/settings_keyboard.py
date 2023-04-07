from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.database.pref_requests import get_preferences


def get_settings_keyboard(user):
    settings_keyboard = InlineKeyboardMarkup(row_width=1)

    user_prefs = get_preferences(user)

    additional_param = 'Так' if user_prefs['additional_courses'] else 'Ні'
    morning_param = 'Так' if user_prefs['morning_schedule'] else 'Ні'
    additional_courses = InlineKeyboardButton(text=f"Показувати повторні курси: {additional_param}",
                                              callback_data='additional_courses')
    morning_schedule = InlineKeyboardButton(text=f"Надсилати розклад зранку: {morning_param}",
                                            callback_data='morning_schedule')

    return settings_keyboard.add(additional_courses).add(morning_schedule)
