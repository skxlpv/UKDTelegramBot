import datetime
import logging

from bot.keyboards.reply.course_keyboard import course_keyboard
from bot.keyboards.reply.group_keyboard import group_keyboard
from bot.keyboards.reply.specialties_keyboard import specialties_keyboard
from bot.keyboards.reply.teacher_keyboard import teacher_keyboard
from bot.utils.api_requests import departments
from bot.utils.get_today_date import get_today_date

teacher_list = []
teacher_buttons_set = set()

curr_year = get_today_date().year - 2000  # Remove thousands, keep only tens
year_set = set()
courses_list = []
groups_list = []
stationary_list = []
specialties_list = []
list_of_all_keyboards = [
    specialties_keyboard,
    course_keyboard,
    group_keyboard,
    teacher_keyboard
]


def get_stationary():
    for value in range(len(departments)):
        group = departments[value]['name']
        title = "".join([ch for ch in group if ch.isalpha()])

        if title.endswith('с'):
            stationary_list.append(group)

    return stationary_list


specialities_dict = {
    "А": "191 Архітектура (Б)",
    "МА": "191 Архітектура (М)",
    "ДФА": "191 Архітектура (ДФ)",

    "Б": "192 Будівництво (Б)",
    "МБ": "192 Будівництво (М)",

    "ГРС": "241 Готельно-ресторанна справа (Б)",

    "Д": "022 Дизайн (Б)",
    "МД": "022 Дизайн (М)",

    "ДФЕ": "151 Економіка (ДФ)",

    "Ж": "061 Журналістика (Б)",

    "ІПЗ": "121 Інженерія ПЗ (Б)",
    "МІПЗ": "121 Інженерія ПЗ (М)",

    "Мн": "073 Менеджмент (Б)",
    "ММ": "025 Музичне мистецтво (Б)",

    "О": "071 Облік та оподаткування (Б)",

    "ПТБ": "076 Підриємництво (Б)",
    "МПТ": "076 Підприємництво (М)",

    "МЮ": "081 Право (М)",
    "Ю": "081 Право (Б)",
    "ДФЮ": "081 Право (ДФ)",

    "Т": "242 Туризм (Б)",

    "ФБС": "072 Фінанси (Б)",
    "МФБ": "072 Фінанси (М)",

    "ФІЛ": "035 Філологія (Б)",

    "Ак": "Ак (Б)",
}


def insert_buttons():
    sorted(specialities_dict)

    for each in specialities_dict.values():
        specialties_keyboard.insert(each)


def clear_keyboard(keyboard_to_be_cleaned):
    for key, value in keyboard_to_be_cleaned.values.copy().items():
        if key == 'keyboard':
            keyboard_to_be_cleaned.values[key].clear()


def clear_all_keyboards(list_of_keyboards=None):
    if list_of_keyboards is None:
        list_of_keyboards = list_of_all_keyboards

    for keyboard in list_of_keyboards:
        clear_keyboard(keyboard)
