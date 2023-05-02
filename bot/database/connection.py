from dotenv import load_dotenv

from bot.database import db

load_dotenv()


def get_schedule_picked():
    col = db['schedule_picked']
    return col


def get_user_pref():
    col = db['user_preferences']
    return col
