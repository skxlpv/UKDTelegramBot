from bot.database.serializers import process_text, validate_favorites_quantity
from bot.database.connection import get_schedule_picked as get_collection
from bot.utils.decorators import update_lact_active


@update_lact_active
def get_from_collection(user, action):
    col = get_collection()
    if action not in ('primary', 'favorites'):
        return -100
    query = {'user_id': user, f"{action}": {"$exists": True}}
    result = col.find_one(query)
    if not result or result == []:
        return -20
    return result[f'{action}']


@update_lact_active
def set_favorites(user, group_name, isTeacher=False):
    col = get_collection()
    insert_data = process_text(group_name, isTeacher)
    if insert_data not in (-1, 'Not implemented'):
        validation = validate_favorites_quantity(user)
        if validation == 1:
            col.update_one({'user_id': user},
                           {'$push':
                               {
                                   "favorites": insert_data
                               }
                            }, upsert=True)
            return 1
        return validation
    return insert_data


@update_lact_active
def set_primary(user, group_name, isTeacher=False):
    col = get_collection()
    insert_data = process_text(group_name, isTeacher)
    if insert_data not in (-1, 'Not implemented'):
        col.update_one({"user_id": user},
                       {'$set':
                           {
                               "primary": insert_data
                           }
                        }, upsert=True)
        return 1
    return -1


@update_lact_active
def delete_favorite(user, group_name):
    col = get_collection()

    col.update_one({'user_id': user},
                   {'$pull':
                       {
                           "favorites":
                               {'$or': [{'teacher_name': group_name}, {'group_name': group_name}]}
                       }
                    })

    return 1
