from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup

from bot.storage.placeholders import buttons

button_role_student = InlineKeyboardButton(text=buttons.STUDENT, callback_data='student')
button_role_teacher = InlineKeyboardButton(text=buttons.TEACHER, callback_data='teacher')
role_keyboard = InlineKeyboardMarkup().add(
    button_role_student, button_role_teacher
)
