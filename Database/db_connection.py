import os

from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


def get_database():
    CONNECTION_STRING = os.environ.get('DATABASE_URL')

    client = MongoClient(CONNECTION_STRING)
    return client['user']


def set_favorites(user, group_name, group_id, isTeacher=False):
    client = get_database()
    col = client['schedule_picked']

    if not isTeacher:
        insert_data = {'group_id': group_id,
                       'group_name': group_name}
    else:
        insert_data = {'teacher_id': group_id,
                       'teacher_name': group_name}

    query = {'user_id': user, "favorites": {"$exists": True}}
    result = col.find_one(query)
    if len(result['favorites']) >= 10:
        return 10

    col.update_one({'user_id': user},
                   {'$push':
                        {"favorites": insert_data}
                    }, upsert=True)

    return 1


def set_primary(user, group_name, group_id, isTeacher=False):
    client = get_database()
    col = client['schedule_picked']
    col.create_index('user_id', unique=True)
    if not isTeacher:
        insert_data = {'group_id': group_id,
                       'group_name': group_name}
    else:
        insert_data = {'teacher_id': group_id,
                       'teacher_name': group_name}

    col.update_one({"user_id": user}, {'$set': {"primary": insert_data}}, upsert=True)
    return 1


def get_favorites(user):
    client = get_database()
    col = client['schedule_picked']
    query = {'user_id': user, "favorites": {"$exists": True}}
    result = col.find_one(query)
    if not result:
        return 20
    return result['favorites']


def get_primary(user):
    client = get_database()
    col = client['schedule_picked']
    query = {'user_id': user, "primary": {"$exists": True}}
    result = col.find_one(query)
    if not result:
        return 20
    return result['primary']


def delete_favorite(user, group_name):
    client = get_database()
    col = client['schedule_picked']
    pass


def drop_db():
    client = get_database()
    col = client['schedule_picked']
    col.drop()
