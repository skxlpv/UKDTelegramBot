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
    0: 'Понеділок',
    1: 'Вівторок',
    2: 'Середа',
    3: 'Четвер',
    4: 'П\'ятниця',
    5: 'Субота',
    6: 'Неділя',
}


def my_schedule_func(group_id, isTeacher, time_str=datetime.now().strftime('%d.%m.%Y')):
    if isTeacher:
        url = f'http://195.162.83.28/cgi-bin/timetable_export.cgi?req_type=rozklad&req_mode=teacher&OBJ_ID={group_id}' \
              f'&OBJ_name=&dep_name=&ros_text=separated&begin_date={time_str}&end_date={time_str}' \
              f'&req_format=json&coding_mode=UTF8&bs=ok'
    else:
        url = f'http://195.162.83.28/cgi-bin/timetable_export.cgi?req_type=rozklad&req_mode=' \
              f'group&OBJ_ID={group_id}&OBJ_name=&dep_name=&ros_text=separated&show_empty=yes&' \
              f'begin_date={time_str}&end_date={time_str}&req_format=json&coding_mode=UTF8&bs=ok'
    data = requests.get(url).json()
    if 'error' in data['psrozklad_export']:
        return data['psrozklad_export']['code']
    data = data['psrozklad_export']['roz_items']
    if data:
        name = ''
        schedule_list = []
        for i in data:
            name = i['object']

        schedule_list.append(f'{name}\n—————')
        for i in data:
            r = f'{i["reservation"]}'
            r = r.replace("<i> <b><small><font color=Navy>", "")
            r = r.replace("</font></small></b></i>", "")
            if i['type'] == "Л":
                emoji = "📖"
            else:
                emoji = "⚒️"
            if i['title'] == "":
                schedule_list.append(f'🕑  {i["lesson_time"]}\n🌀  {r}\n- - - - - - - - -')
            elif i['reservation'] == "":
                schedule_list.append(
                    f'🕑  {i["lesson_time"]}\n{emoji}  {i["title"]}, ({i["type"]})\n👨‍🏫  {i["teacher"]}  '
                    f'{i["room"]}\n- - - - - - - - -')
            else:
                schedule_list.append(
                    f'🕑  {i["lesson_time"]}\n{emoji}  {i["title"]}, ({i["type"]})\n👨‍🏫  {i["teacher"]}  '
                    f'{i["room"]}\n🌀  {r}\n- - - - - - - - -')

        string_of_lessons = ''
        for i in schedule_list:
            string_of_lessons += i + '\n'
        final_string_of_lessons = remove_last_line_from_string(string_of_lessons)
        return final_string_of_lessons
    else:
        return None


def my_schedule_big_func(group_id, isTeacher, firstday, lastday):
    fday = firstday
    count = 0
    schedule_list = []
    while fday < lastday:
        time_str = fday.strftime('%d.%m.%Y')

        if isTeacher:
            url = f'http://195.162.83.28/cgi-bin/timetable_export.cgi?req_type=rozklad&req_mode=teacher&OBJ_ID={group_id}' \
                  f'&OBJ_name=&dep_name=&ros_text=separated&begin_date={time_str}&end_date={time_str}' \
                  f'&req_format=json&coding_mode=UTF8&bs=ok'
        else:
            url = f'http://195.162.83.28/cgi-bin/timetable_export.cgi?req_type=rozklad&req_mode=' \
                  f'group&OBJ_ID={group_id}&OBJ_name=&dep_name=&ros_text=separated&show_empty=yes&' \
                  f'begin_date={time_str}&end_date={time_str}&req_format=json&coding_mode=UTF8&bs=ok'
        data = requests.get(url).json()
        data = data['psrozklad_export']['roz_items']
        # data = await state.get_data('data')
        # data = data['data']['psrozklad_export']['roz_items']
        name_day = name_day_of_week(count)

        schedule_list.append(f'{name_day}\n\n- - - - - - - - -')

        for i in data:

            r = f'{i["reservation"]}'
            r = r.replace("<i> <b><small><font color=Navy>", "")
            r = r.replace("</font></small></b></i>", "")
            if i['type'] == "Л":
                emoji = "📖"
            else:
                emoji = "⚒️"
            if i['title'] == "":
                schedule_list.append(f'🕑  {i["lesson_time"]}\n🌀  {r}\n- - - - - - - - -')
            elif i['reservation'] == "":
                schedule_list.append(
                    f'🕑  {i["lesson_time"]}\n{emoji}  {i["title"]}, ({i["type"]})\n👨‍🏫  {i["teacher"]}  '
                    f'{i["room"]}\n- - - - - - - - -')
            else:
                schedule_list.append(
                    f'🕑  {i["lesson_time"]}\n{emoji}  {i["title"]}, ({i["type"]})\n👨‍🏫  {i["teacher"]}  '
                    f'{i["room"]}\n🌀  {r}\n- - - - - - - - -')

        fday = fday + timedelta(days=1)
        count += 1
    string_of_lessons = ''
    for i in schedule_list:
        string_of_lessons += i + '\n'
    final_string_of_lessons = remove_last_line_from_string(string_of_lessons)
    return final_string_of_lessons


def name_func(group_id, isTeacher):
    time_str = ''
    day = datetime.now().weekday()
    if day == 5 or day == 6:
        time = datetime.now() - timedelta(days=2)
        time_str = time.strftime('%d.%m.%Y')

    if isTeacher:
        url = f'http://195.162.83.28/cgi-bin/timetable_export.cgi?req_type=rozklad&req_mode=teacher&OBJ_ID={group_id}' \
              f'&OBJ_name=&dep_name=&ros_text=separated&begin_date={time_str}&end_date={time_str}' \
              f'&req_format=json&coding_mode=UTF8&bs=ok'
    else:
        url = f'http://195.162.83.28/cgi-bin/timetable_export.cgi?req_type=rozklad&req_mode=' \
              f'group&OBJ_ID={group_id}&OBJ_name=&dep_name=&ros_text=separated&show_empty=yes&' \
              f'begin_date={time_str}&end_date={time_str}&req_format=json&coding_mode=UTF8&bs=ok'
    data = requests.get(url).json()
    data = data['psrozklad_export']['roz_items']
    name = ''
    for i in data:
        name = i["object"]
    return name


def name_day_of_week(count):
    if count == 0:
        name = "Понеділок"
        return name
    elif count == 1:
        name = f'\nВівторок'
        return name
    elif count == 2:
        name = f'\nСереда'
        return name
    elif count == 3:
        name = f'\nЧетвер'
        return name
    elif count == 4:
        name = f"\nП'ятниця"
        return name


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
            if await validate_primary(user=message.from_user.id, isTeacher=isTeacher, schedule=schedule):
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
            if await validate_primary(user=message.from_user.id, isTeacher=isTeacher, schedule=schedule):
                keyboard = get_schedule_keyboard(user=message.from_user.id, group_id=group_id, isTeacher=isTeacher)
                await message.answer(schedule, parse_mode='HTML', reply_markup=keyboard)
                await UserStates.schedule_callback.set()
    else:  # if primary DOES NOT EXIST
        return False


async def week_schedule_display(week, callback, group_id, isTeacher, state: FSMContext, today=datetime.now()):
    weekday = today.weekday()
    data = await state.get_data()
    search_name = data['search_name']

    if week == 'current':
        monday = today - timedelta(days=weekday)
        current_friday = today - timedelta(days=(-weekday - 4))
    elif week == 'next':
        monday = today - timedelta(days=weekday - 7)
        current_friday = monday + timedelta(days=4)
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
        keyboard = get_schedule_keyboard(user=callback.from_user.id, group_id=group_id, isTeacher=isTeacher)
        await callback.message.edit_text(text=schedule, parse_mode='HTML', reply_markup=keyboard)
    except aiogram.utils.exceptions.MessageNotModified:
        pass


async def validate_primary(user, isTeacher, schedule):
    if schedule in ('90',):
        await bot.send_message(chat_id=user,
                               text='Вибачте, даний розклад не знайдено чи було видалено',
                               reply_markup=menu_keyboard)
        await UserStates.menu_handler.set()
        delete_primary(user=user, isTeacher=isTeacher)
        return False
    return True
