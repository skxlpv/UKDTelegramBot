from bot.database.connection import get_user_pref as get_collection
from datetime import datetime

from bot.utils import update_lact_active

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


@update_lact_active
def get_preferences(user):
    col = get_collection()
    request = col.find_one({'user_id': user})
    return request['mutable']


@update_lact_active
def toggle_pref(user, param):
    col = get_collection()
    query = {'user_id': user}
    toggle = [{'$set':
         {f'mutable.{param}':
            {'$switch':
                {'branches': [
                    {'case':
                         {'$eq':
                              [f'$mutable.{param}', True]
                          }, 'then': False
                     },
                    {'case':
                         {'$eq':
                              [f'$mutable.{param}', False]
                          }, 'then': True
                     }],
                }
            }
        }
    }]
    if param in DEFAULT_VALUES:
        col.update_one(query, toggle)
        return 1
    return -100
