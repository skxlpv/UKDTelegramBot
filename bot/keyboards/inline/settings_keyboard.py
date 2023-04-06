from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

menu = InlineKeyboardButton(text='Меню', callback_data='menu')

def get_settings_keyboard(user):
    settings_keyboard = InlineKeyboardMarkup(row_width=1)
    additional_courses = InlineKeyboardButton(text="Показувати повторні курси", callback_data='additional_courses')
    morning_schedule = InlineKeyboardButton(text="Надсилати розклад зранку", callback_data='morning_schedule')
    # show_facts = InlineKeyboardButton(text="Показувати цікаві факти", callback_data='show_facts')
    return settings_keyboard.add(additional_courses).add(morning_schedule).add(menu)
