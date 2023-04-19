import datetime

from bot.keyboards.reply.course_keyboard import course_keyboard
from bot.keyboards.reply.group_keyboard import group_keyboard
from bot.keyboards.reply.specialties_keyboard import specialties_keyboard
from bot.keyboards.reply.teacher_keyboard import teacher_keyboard
from bot.utils.api_requests import departments

teacher_list = []
teacher_buttons_set = set()

curr_year = datetime.date.today().year - 2000   # Remove thousands, keep only tens
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


def get_specialty_titles():
    titles_set = set()
    for value in range(len(departments)):
        group_name = departments[value]['name']
        title = "".join([ch for ch in group_name if ch.isalpha()])

        if title.endswith('с'):
            title = title[:-1]
            titles_set.add(title)

    return sorted(titles_set)


def shrank_specialties_list():
    return list(get_specialty_titles())


def insert_buttons(buttons_set=None):
    if buttons_set is None:
        buttons_set = get_specialty_titles()
    for each in buttons_set:
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
