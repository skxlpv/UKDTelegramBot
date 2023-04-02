from datetime import datetime

from aiogram import Bot
from dateutil.relativedelta import relativedelta

from bot.database.connection import get_user_pref, get_schedule_picked
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
            await bot.send_message(user_id, f'Твій розклад на сьогодні: Not implemented YET')


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
