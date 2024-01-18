from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup

from bot.storage.placeholders import buttons

button_role_student = InlineKeyboardButton(text=buttons.STUDENT, callback_data='student')
button_role_teacher = InlineKeyboardButton(text=buttons.TEACHER, callback_data='teacher')
role_keyboard = InlineKeyboardMarkup().add(
    button_role_student, button_role_teacher
)


button_stationary = InlineKeyboardButton(buttons.STATIONARY, callback_data='stationary')
button_dual = InlineKeyboardButton(buttons.DUAL, callback_data='dual')
degree_type_keyboard = InlineKeyboardMarkup().add(
    button_stationary, button_dual
)


button_university = InlineKeyboardButton(buttons.UNIVERSITY, callback_data='university')
button_college = InlineKeyboardButton(buttons.COLLEGE, callback_data='college')
institution_keyboard = InlineKeyboardMarkup().add(
    button_university, button_college
)
