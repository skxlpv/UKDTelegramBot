from datetime import datetime, timedelta

import aiogram.utils.exceptions
import requests
from aiogram import Bot
from aiogram.dispatcher import FSMContext

from bot.database.schedule_requests import delete_primary
from bot.keyboards.inline.schedule_keyboard import get_schedule_keyboard
from bot.keyboards.reply.menu_keyboard import menu_keyboard
from bot.states.UserStates import UserStates
from bot.utils import render_schedule
from configs import API_TOKEN

bot = Bot(token=API_TOKEN)

day_of_week_dict = {
    0: 'ПОНЕДІЛОК',
    1: 'ВІВТОРОК',
    2: 'СЕРЕДА',
    3: 'ЧЕТВЕР',
    4: 'П\'ЯТНИЦЯ',
    5: 'СУБОТА',
    6: 'НЕДІЛЯ',
}


async def get_teacher_or_group(primary, message, state):
    if primary != -20:  # if primary EXISTS
        if 'teacher_name' in primary:
            isTeacher = True
            group_id = primary['teacher_id']
            today_date = datetime.today().strftime("%d.%m.%Y")
            schedule = await render_schedule.render_schedule(search_name=primary['teacher_name'], search_id=group_id,
                                                             begin_date=today_date, end_date=today_date,
                                                             isTeacher=isTeacher, state=state)
            # if schedule validated (primary exist)
            if await schedule_exist(user=message.from_user.id, isTeacher=isTeacher, schedule=schedule):
                await bot.send_message(chat_id=message.from_user.id, text='Ваш розклад:', reply_markup=menu_keyboard)
                keyboard = get_schedule_keyboard(user=message.from_user.id, group_id=group_id, isTeacher=isTeacher)
                await message.answer(schedule, parse_mode='HTML', reply_markup=keyboard)
                await UserStates.schedule_callback.set()
        else:
            isTeacher = False
            group_id = primary['group_id']
            today_date = datetime.today().strftime("%d.%m.%Y")
            schedule = await render_schedule.render_schedule(search_name=primary['group_name'], search_id=group_id,
                                                             begin_date=today_date,
                                                             end_date=today_date, isTeacher=isTeacher, state=state)
            # if schedule validated (primary exist)
            if await schedule_exist(user=message.from_user.id, isTeacher=isTeacher, schedule=schedule):
                await bot.send_message(chat_id=message.from_user.id, text='Ваш розклад:', reply_markup=menu_keyboard)
                keyboard = get_schedule_keyboard(user=message.from_user.id, group_id=group_id, isTeacher=isTeacher)
                await message.answer(schedule, parse_mode='HTML', reply_markup=keyboard)
                await UserStates.schedule_callback.set()
    else:  # if primary DOES NOT EXIST
        return False


async def week_schedule_display(week, callback, group_id, isTeacher, state: FSMContext, today=datetime.today()):
    weekday = today.weekday()
    data = await state.get_data()
    search_name = data['search_name']

    if week == 'current':
        monday = today - timedelta(days=weekday)
        current_friday = monday + timedelta(days=5)
    elif week == 'next':
        monday = today - timedelta(days=weekday - 7)
        current_friday = monday + timedelta(days=5)
    else:
        print('Week argument in week_schedule_display() is invalid. '
              'Must be either "current" or "next"')
        raise ValueError

    schedule = await render_schedule.render_schedule(search_name=search_name, search_id=group_id,
                                                     begin_date=monday.strftime('%d.%m.%Y'),
                                                     end_date=current_friday.strftime('%d.%m.%Y'),
                                                     isTeacher=isTeacher, state=state)
    try:
        await callback.message.edit_text(text=schedule, parse_mode='HTML',
                                         reply_markup=get_schedule_keyboard(user=callback.from_user.id,
                                                                            group_id=group_id, isTeacher=isTeacher))
    except aiogram.utils.exceptions.MessageNotModified:
        pass


async def day_schedule_display(number, callback, group_id, isTeacher, state: FSMContext, today=datetime.now()):
    weekday = today.weekday()
    data = await state.get_data()
    search_name = data['search_name']

    monday = today - timedelta(days=(weekday - number))
    date = monday.strftime('%d.%m.%Y')

    schedule = await render_schedule.render_schedule(search_name=search_name, search_id=group_id,
                                                     begin_date=date, end_date=date,
                                                     isTeacher=isTeacher, state=state)
    try:
        keyboard = get_schedule_keyboard(user=callback.from_user.id, group_id=group_id,
                                         isTeacher=isTeacher, weekday=number)
        await callback.message.edit_text(text=schedule, parse_mode='HTML', reply_markup=keyboard)
    except aiogram.utils.exceptions.MessageNotModified:
        pass


async def schedule_exist(user, isTeacher, schedule):
    if schedule in ('90',):
        await bot.send_message(chat_id=user,
                               text='Вибачте, даний розклад не знайдено чи було видалено',
                               reply_markup=menu_keyboard)
        await UserStates.menu_handler.set()
        delete_primary(user=user, isTeacher=isTeacher)
        return False
    return True
