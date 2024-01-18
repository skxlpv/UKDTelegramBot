from bot.keyboards.reply.course_keyboard import course_keyboard
from bot.keyboards.reply.group_keyboard import group_keyboard
from bot.keyboards.reply.specialties_keyboard import specialties_keyboard
from bot.keyboards.reply.teacher_keyboard import teacher_keyboard
from bot.utils.api_requests import get_departments
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


specialities_dict = {
    "А": "Архітектура",
    "Ак": "Архітектура (Акс)",
    "ДФА": "Архітектура (ДФ)",

    "Б": "Будівництво",

    "ГРС": "Готельно-ресторанна справа",

    "Д": "Дизайн",

    "ДФЕ": "Економіка (ДФ)",

    "Ж": "Журналістика",

    "ІПЗ": "Інженерія ПЗ",

    "Мн": "Менеджмент",
    "ММ": "Музичне мистецтво",

    "О": "Облік та оподаткування",

    "ПТБ": "Підриємництво",

    "Ю": "Право",
    "ДФЮ": "Право (ДФ)",

    "Т": "Туризм",

    "ФБС": "Фінанси",

    "ФІЛ": "Філологія",
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
