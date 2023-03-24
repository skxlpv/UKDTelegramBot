from bot.utils.api_requests import departments
from bot.database.connection import get_schedule_picked as get_collection
from bot.database import schedule_requests as request


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
    favorites = request.get_from_collection(user, 'favorites')
    if favorites not in (-20, []):
        if len(favorites) >= 10:
            return -10

    return 1
