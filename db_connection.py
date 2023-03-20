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

    if not col.find_one({"_id": user}):

        user_data = {
            '_id': user,
            'primary': '',
            'favorites': [insert_data]
        }
        col.insert_one(user_data)
    else:
        old_data = col.find_one({"_id": user})
        if len(old_data['favorites']) >= 10:
            return 0
        new = old_data['favorites']
        new.append(insert_data)
        col.find_one_and_update({"_id": user}, {'$set': {"favorites": new}})


def set_primary(user, group_name, group_id, isTeacher=False):
    client = get_database()
    col = client['schedule_picked']

    if not isTeacher:
        insert_data = {'group_id': group_id,
                       'group_name': group_name}
    else:
        insert_data = {'teacher_id': group_id,
                       'teacher_name': group_name}

    if not col.find_one({"_id": user}):
        user_data = {
            '_id': user,
            'primary': insert_data,
            'favorites': []
        }
        col.insert_one(user_data)
    else:
        col.find_one_and_update({"_id": user}, {'$set': {"primary": insert_data}})


def get_favorites(user):
    client = get_database()
    col = client['schedule_picked']
    if not col.find_one({"_id": user}):
        return 0
    result = col.find_one({'_id': user})['favorites']
    return result


def get_primary(user):
    client = get_database()
    col = client['schedule_picked']
    if not col.find_one({"_id": user}):
        return 0
    primary = col.find_one({'_id': user})['primary']
    return primary


def drop_db():
    client = get_database()
    col = client['schedule_picked']
    col.drop()
