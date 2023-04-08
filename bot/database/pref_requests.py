from bot.database.connection import get_user_pref as get_collection

from bot.utils import update_lact_active, DEFAULT_VALUES
from loader import logger


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
    logger.error(f'ERROR occurred while toggle_pref: -100')
    return -100
