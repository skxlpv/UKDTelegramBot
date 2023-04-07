from datetime import datetime

from aiogram import Bot
from aiogram.utils.exceptions import ChatNotFound
from dateutil.relativedelta import relativedelta

from bot.database.connection import get_user_pref, get_schedule_picked
from bot.database.schedule_requests import get_from_collection
from bot.utils.render_schedule import get_schedule
from configs import API_TOKEN

bot = Bot(token=API_TOKEN)


async def send_daily_schedule():
    col_pref = get_user_pref()
    col_schedule = get_schedule_picked()

    users = col_pref.find()

    for user in users:
        user_id = user['user_id']
        pref = user['mutable']['morning_schedule']
        if pref is True:
            user_primary = get_from_collection(user=user_id, action='primary')
            if user_primary != -20:
                if 'group_id' in user_primary:
                    group_id = user_primary['group_id']
                    group_name = user_primary['group_name']
                    isTeacher = False
                else:
                    group_id = user_primary['teacher_id']
                    group_name = user_primary['teacher_name']
                    isTeacher = True
                text = get_schedule(search_name=group_name, search_id=group_id, isTeacher=isTeacher)
                if text is None or text == '90':
                    continue
                else:
                    try:
                        await bot.send_message(chat_id=user_id, text=text, parse_mode='HTML')
                    except ChatNotFound:
                        col_schedule.find_one_and_delete({'user_id': user_id})
                        col_pref.find_one_and_delete({'user_id': user_id})
            else:
                continue


async def database_cleanup():
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
