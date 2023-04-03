from dotenv import load_dotenv
from pymongo import MongoClient

from configs import CONNECTION_STRING

load_dotenv()


def get_database():
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


def close_connection():
    client = get_database().client
    client.close()
