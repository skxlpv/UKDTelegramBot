from bot.utils.api_requests import departments
from connection import get_schedule_picked as get_collection
from schedule_requests import get_from_collection


def process_text(group_name, isTeacher=False):
    group_name = group_name.lower()
    if not isTeacher:
        for index in range(len(departments)):
            if group_name.lower() == departments[index]['name'].lower():
                group_name = departments[index]['name']
                group_id = departments[index]['ID']
                return {'group_id': group_id,
                        'group_name': group_name}
    else:
        return 'Not implemented'
    return -1


def validate_favorites_quantity(user):
    favorites = get_from_collection(user, 'favorites')
    if favorites not in (-20, []):
        if len(favorites) >= 10:
            return -10

    return 1


def get_insert_data(group_name, group_id, isTeacher=False):
    if not isTeacher:
        insert_data = {'group_id': group_id,
                       'group_name': group_name}
    else:
        insert_data = {'teacher_id': group_id,
                       'teacher_name': group_name}
    return insert_data
