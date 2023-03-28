from bot.database.connection import get_user_pref as get_collection
from datetime import datetime


DEFAULT_VALUES = {'additional_courses': False,
                  'morning_schedule': True,
                  'show_facts': False}

def initialize_user_pref(user):
    col = get_collection()
    today = datetime.today()
    date = datetime(today.year, today.month, today.day)
    init_data = {'mutable': DEFAULT_VALUES,
                 'last_active': date}
    col.update_one({'user_id': user}, {'$set': init_data}, upsert=True)


def update_lact_active(func):
    def wrapper_func(*args, **kwargs):

        col = get_collection()
        today = datetime.today()
        date = datetime(today.year, today.month, today.day)
        user = kwargs['user'] if 'user' in kwargs else args[0]
        if col.find_one_and_update({'user_id': user}, {'$set': {'last_active': date}}) is None:
            initialize_user_pref(user)

        return func(*args, **kwargs)

    return wrapper_func


