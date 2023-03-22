from bot.keyboards.reply.specialties_keyboard import specialties_keyboard
from bot.utils.api_requests import departments

year_set = set()
courses_list = []
groups_list = []
stationary_list = []
specialties_list = []

list_of_courses = {
    '1': '1 курс',
    '2': '2 курс',
    '3': '3 курс',
    '4': '4 курс'
}

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

        if title.endswith('с') or title.endswith('д') or title.endswith('з'):
            title = title[:-1]

        titles_set.add(title)
    return sorted(titles_set)


shrinked_specialties_list = list(get_specialty_titles())


def insert_buttons(buttons_set=None):
    if buttons_set is None:
        buttons_set = get_specialty_titles()
    for each in buttons_set:
        specialties_keyboard.insert(each)
