from dotenv import load_dotenv

from bot.database import client

load_dotenv()


def get_database():
    return client['user']


def get_schedule_picked():
    client = get_database()
    col = client['schedule_picked']
    return col


def get_user_pref():
    client = get_database()
    col = client['user_preferences']
    return col
