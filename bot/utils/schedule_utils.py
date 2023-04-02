from datetime import datetime, timedelta

import requests

from bot.handlers import show_schedule
from bot.keyboards.inline.schedule_keyboard import schedule_keyboard


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
                schedule_list.append(f'🕑  {i["lesson_time"]}\n{emoji}  {i["title"]}, ({i["type"]})\n👨‍🏫  {i["teacher"]}  '
                                     f'{i["room"]}\n- - - - - - - - -')
            else:
                schedule_list.append(f'🕑  {i["lesson_time"]}\n{emoji}  {i["title"]}, ({i["type"]})\n👨‍🏫  {i["teacher"]}  '
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
                schedule_list.append(f'🕑  {i["lesson_time"]}\n{emoji}  {i["title"]}, ({i["type"]})\n👨‍🏫  {i["teacher"]}  '
                                     f'{i["room"]}\n- - - - - - - - -')
            else:
                schedule_list.append(f'🕑  {i["lesson_time"]}\n{emoji}  {i["title"]}, ({i["type"]})\n👨‍🏫  {i["teacher"]}  '
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
            await show_schedule.my_schedule(chat_id=message.chat.id, state=state,
                                            group_id=group_id, isTeacher=isTeacher)
        else:
            isTeacher = False
            group_id = primary['group_id']
            await show_schedule.my_schedule(chat_id=message.chat.id, state=state,
                                            group_id=group_id, isTeacher=isTeacher)
    else:  # if primary DOES NOT EXIST
        return False


async def week_schedule_display(week, callback, group, isTeacher, today=datetime.now()):
    weekday = today.weekday()

    if week == 'current':
        current_or_next = 'поточний'
        monday = today - timedelta(days=weekday)
        current_friday = today - timedelta(days=(-weekday - 4))
        friday = today - timedelta(days=(-weekday - 5))
    elif week == 'next':
        current_or_next = 'наступний'
        monday = today - timedelta(days=weekday - 7)
        current_friday = today - timedelta(days=(-weekday - 1))
        friday = today - timedelta(days=(-weekday - 2))
    else:
        print('Week argument in week_schedule_display() is invalid. '
              'Must be either "current" or "next"')
        raise ValueError

    name = name_func(group, isTeacher)
    final_string_of_lessons = my_schedule_big_func(group, isTeacher, monday, friday)
    await callback.message.edit_text(text=f"Розклад на {current_or_next} тиждень\nдля {name}, з "
                                          f"{monday.strftime('%d.%m')} по {current_friday.strftime('%d.%m')}"
                                          f"\n—————\n\n{final_string_of_lessons}", reply_markup=schedule_keyboard)


async def day_schedule_display(number, day_of_week, callback, group, isTeacher, today=datetime.now()):
    weekday = today.weekday()

    monday = today - timedelta(days=(weekday - number))
    time_str = monday.strftime('%d.%m.%Y')
    final_string_of_lessons = my_schedule_func(group_id=group, isTeacher=isTeacher, time_str=time_str)
    await callback.message.edit_text(text=f'{day_of_week} - {monday.strftime("%d.%m")}\n'
                                          f'{final_string_of_lessons}', reply_markup=schedule_keyboard)


def remove_last_line_from_string(final_string_of_lessons):
    return final_string_of_lessons[:final_string_of_lessons.rfind('\n- - - - - - - - -')]
