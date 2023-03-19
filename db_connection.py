import os

from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


def get_database():
    CONNECTION_STRING = os.environ.get('DATABASE_URL')

    client = MongoClient(CONNECTION_STRING)
    return client['user']


def set_favorites(data):
    client = get_database()
    col = client['schedule_picked']

    if not col.find_one({"_id": data.chat["id"]}):

        user_data = {
            '_id': data.chat['id'],
            'primary': '',
            'favorites': [data.text]
        }
        col.insert_one(user_data)
    else:
        old_data = col.find_one({"_id": data.chat["id"]})
        new = old_data['favorites']
        new.append(data.text)
        col.find_one_and_update({"_id": data.chat["id"]}, {'$set': {"favorites": new}})


def set_primary(data):
    client = get_database()
    col = client['schedule_picked']

    if not col.find_one({"_id": data.chat["id"]}):
        user_data = {
            '_id': data.chat['id'],
            'primary': data.text,
            'favorites': []
        }
        col.insert_one(user_data)
    else:
        col.find_one_and_update({"_id": data.chat["id"]}, {'$set': {"primary": data.text}})


def get_favorites(data):
    client = get_database()
    col = client['schedule_picked']
    if not col.find_one({"_id": data.chat["id"]}):
        return 0
    result = col.find_one({'_id': data.chat['id']})['favorites']
    return result


def get_primary(data):
    client = get_database()
    col = client['schedule_picked']
    if not col.find_one({"_id": data.chat["id"]}):
        return 0
    primary = col.find_one({'_id': data.chat['id']})['primary']
    return primary


def drop_db():
    client = get_database()
    col = client['schedule_picked']
    col.drop()
