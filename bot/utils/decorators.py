from bot.database.connection import get_user_pref as get_collection
from datetime import datetime

from bot import database


def update_lact_active(func):
    def wrapper_func(*args, **kwargs):

        col = get_collection()
        today = datetime.today()
        date = datetime(today.year, today.month, today.day)
        user = kwargs['user'] if 'user' in kwargs else args[0]
        if col.find_one_and_update({'user_id': user}, {'$set': {'last_active': date}}) is None:
            database.pref_requests.initialize_user_pref(user)

        return func(*args, **kwargs)

    return wrapper_func
