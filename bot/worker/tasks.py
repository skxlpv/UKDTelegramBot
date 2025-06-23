from datetime import datetime

from aiogram import Bot
from aiogram.utils.exceptions import ChatNotFound, BotBlocked
from dateutil.relativedelta import relativedelta

import loader
from bot.database import schedule_requests
from bot.database.connection import get_user_pref, get_schedule_picked
from bot.utils.render_schedule import get_schedule
from configs import API_TOKEN

bot = Bot(token=API_TOKEN)


async def send_daily_schedule():
    loader.logger.info('WORKER: method "send_daily_schedule" started')
    col_pref = get_user_pref()
    col_schedule = get_schedule_picked()

    users = col_pref.find()

    for user in users:
        loader.logger.disabled = True
        user_id = user['user_id']
        pref = user['mutable']['morning_schedule']
        if pref is True:
            user_primary = schedule_requests.get_from_collection(user=user_id, action='primary')
            if user_primary != -20:
                if 'group_id' in user_primary:
                    group_id = user_primary['group_id']
                    group_name = user_primary['group_name']
                    isTeacher = False
                else:
                    group_id = user_primary['teacher_id']
                    group_name = user_primary['teacher_name']
                    isTeacher = True
                text = get_schedule(search_name=group_name, search_id=group_id, isTeacher=isTeacher, user_id=user_id)
                if text is None or text.isnumeric():
                    continue
                else:
                    try:
                        await bot.send_message(chat_id=user_id, text=text, parse_mode='HTML', disable_web_page_preview=True)
                    except (ChatNotFound, BotBlocked) as ex:
                        col_schedule.find_one_and_delete({'user_id': user_id})
                        col_pref.find_one_and_delete({'user_id': user_id})
                        loader.logger.disabled = False
                        loader.logger.error(f'FAILED daily schedule sending. EXCEPTION: {ex}. User: {user_id} deleted')
                        loader.logger.disabled = True
                        continue
            else:
                continue
    loader.logger.disabled = False
    loader.logger.info('WORKER: method "send_daily_schedule" ended')


async def database_cleanup():
    loader.logger.info('WORKER: method "database_cleanup" started')
    col_pref = get_user_pref()
    col_schedule = get_schedule_picked()

    users = col_pref.find()

    data_six_month_before = datetime.now() - relativedelta(months=+6)
    for user in users:
        user_id = user['user_id']
        last_active = user['last_active']
        if last_active < data_six_month_before:
            col_schedule.find_one_and_delete({'user_id': user_id})
            col_pref.find_one_and_delete({'user_id': user_id})
            loader.logger.info(f'User {user_id} (last active: {last_active}) '
                               f'has been deleted during database_cleanup')

    loader.logger.info('WORKER: method database_cleanup" ended')
