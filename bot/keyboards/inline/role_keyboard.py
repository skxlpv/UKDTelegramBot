from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup


button_role_student = InlineKeyboardButton(text='Студент/ка', callback_data='student')
button_role_teacher = InlineKeyboardButton(text='Викладач/ка', callback_data='teacher')
role_keyboard = InlineKeyboardMarkup().add(
    button_role_student, button_role_teacher
)