from bot.database.connection import get_schedule_picked as get_collection
from bot.database.serializers import process_text, validate_favorites_quantity
from bot.utils import update_lact_active
import loader


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
def get_one_if_exist(user, group_id, isTeacher, action):
    col = get_collection()
    if isTeacher:
        id_name = 'teacher_id'
    else:
        id_name = 'group_id'
    if action not in ('primary', 'favorites'):
        return -100
    query = {'user_id': user, f"{action}.{id_name}": group_id}
    result = col.find_one(query)
    return result


@update_lact_active
def set_favorites(user, group_id, isTeacher=False):
    col = get_collection()
    insert_data = process_text(group_id, isTeacher)
    if insert_data not in (-1,):
        validation = validate_favorites_quantity(user, insert_data, isTeacher=isTeacher)
        if validation == 1:
            col.update_one({'user_id': user},
                           {'$push':
                               {
                                   "favorites": insert_data
                               }
                           }, upsert=True)
            loader.logger.info(f'User {user} set favorites: id-{group_id}, teacher-{isTeacher}')
            return 1
        elif validation == -11:
            loader.logger.error(f'User {user} ERROR occurred in set_favorites: {validation}: limit exceed')
        return validation
    loader.logger.error(f'User {user} ERROR occurred in set_favorites: -1: id-{group_id}, teacher-{isTeacher}')
    return insert_data


@update_lact_active
def set_primary(user, group_id, isTeacher=False):
    if get_one_if_exist(user=user, group_id=group_id, isTeacher=isTeacher, action='primary'):
        return -11
    col = get_collection()
    insert_data = process_text(group_id, isTeacher)
    if insert_data not in (-1,):
        col.update_one({"user_id": user},
                       {'$set':
                           {
                               "primary": insert_data
                           }
                       }, upsert=True)
        loader.logger.info(f'User {user} set primary: id-{group_id}, teacher-{isTeacher}')
        return 1
    loader.logger.error(f'User {user} ERROR occurred in set_primary: -1: id-{group_id}, teacher-{isTeacher}')
    return -1


@update_lact_active
def delete_favorite(user, group_id, isTeacher=False):
    col = get_collection()

    if isTeacher:
        col.update_one({'user_id': user},
                       {'$pull':
                           {
                               "favorites":
                                   {'teacher_id': group_id},
                           }
                       })
    else:
        col.update_one({'user_id': user},
                       {'$pull':
                           {
                               "favorites":
                                   {'group_id': group_id},
                           }
                       })
    loader.logger.info(f'User {user} deleted favorite: id-{group_id}, teacher-{isTeacher}')
    return 1


def delete_primary(user):
    col = get_collection()

    col.update_one({'user_id': user},
                   {'$unset':
                       {
                           "primary": 1
                       }
                   })
    loader.logger.info(f'User {user} deleted primary')
    return 1
