import os

from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


def get_database():
    CONNECTION_STRING = os.environ.get('DATABASE_URL')

    client = MongoClient(CONNECTION_STRING)
    return client['user']


def get_schedule_picked():
    client = get_database()
    col = client['schedule_picked']
    return col


def get_user_pref():
    client = get_database()
    col = client['user_preferences']
    return col
