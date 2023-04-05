from bot.database import schedule_requests as request
from bot.utils.api_requests import departments, teachers


def process_text(group_id, isTeacher=False):
    if not isTeacher:
        for index in range(len(departments)):
            if group_id == departments[index]['ID']:
                group_name = departments[index]['name']
                return {'group_id': group_id,
                        'group_name': group_name}
    else:
        for index in range(len(teachers)):
            all_teachers = teachers[index]['objects']
            for i in range(len(all_teachers)):
                teacher = teachers[index]['objects'][i]
                if group_id == teacher['ID']:
                    teacher_name = teacher['name'].replace(" (пог.)", "").replace("*", "")
                    return {'teacher_id': group_id,
                            'teacher_name': teacher_name}
    return -1


def validate_favorites_quantity(user, insert_data, isTeacher):
    if isTeacher:
        group_id = insert_data['teacher_id']
    else:
        group_id = insert_data['group_id']
    if request.get_one_if_exist(user=user, group_id=group_id, isTeacher=isTeacher, action='favorites'):
        return -11
    favorites = request.get_from_collection(user, 'favorites')
    if favorites not in (-20,):

        if len(favorites) >= 10:
            return -10
    return 1
