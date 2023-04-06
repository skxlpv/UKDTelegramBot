from datetime import datetime

import requests
from aiogram.dispatcher import FSMContext

from bot.utils.schedule_utils import day_of_week_dict


async def render_schedule(search_name, search_id, isTeacher, begin_date: datetime.date,
                          end_date: datetime.date, state: FSMContext):
    async with state.proxy() as data:  # put variables in storage
        data['search_name'] = search_name
        data['group_id'] = str(search_id)
        data['isTeacher'] = isTeacher

    schedule = get_schedule(search_name=search_name, search_id=search_id, isTeacher=isTeacher,
                            begin_date=begin_date, end_date=end_date)
    if schedule is None:
        schedule = ''
        schedule += f"<code><u>{search_name}</u></code>\n"
        schedule += 'Цього дня у вас немає пар, хорошого відпочинку!'
    return schedule


def get_schedule(search_name, search_id, isTeacher,
                 begin_date=datetime.now().strftime('%d.%m.%Y'), end_date=datetime.now().strftime('%d.%m.%Y')):
    list_of_lessons = []
    message_of_lessons = ''
    break_line = '_________________________________'
    # perform request based on isTeacher arg
    if isTeacher:
        request_mode = 'teacher'
    else:
        request_mode = 'group'
    obj = requests.get(
        f'http://195.162.83.28/cgi-bin/timetable_export.cgi?req_type=rozklad&req_mode={request_mode}'
        f'&OBJ_ID={search_id}&OBJ_name=&dep_name=&ros_text=separated&begin_date={begin_date}&end_date={end_date}'
        f'&req_format=json&coding_mode=UTF8&bs=ok').json()

    if 'error' in obj['psrozklad_export']:
        return obj['psrozklad_export']['code']

    # generate group title
    today_lessons_list = obj['psrozklad_export']['roz_items']
    list_of_lessons.append(f"<code><u>{search_name}</u></code>")

    schedule_statistics = f'_________________________________\n' \
                          f'<code>Загальна кількість пар: {len(today_lessons_list)}</code>'

    # generate list of lessons
    if len(today_lessons_list) > 0:
        day_of_week = 0
        current_date = 0

        # get values
        for lesson_index in range(len(today_lessons_list)):
            object_date = today_lessons_list[lesson_index]['date']

            if object_date != current_date:
                next_day_of_week = datetime.strptime(object_date, '%d.%m.%Y').weekday()
                list_of_lessons.append(break_line)
                list_of_lessons.append(f'<code><u>{day_of_week_dict[next_day_of_week]}, {object_date}</u></code>')
                current_date = object_date
                day_of_week += next_day_of_week

            time = today_lessons_list[lesson_index]['lesson_time']
            title = today_lessons_list[lesson_index]['title']
            lesson_type = today_lessons_list[lesson_index]['type']
            if isTeacher:
                teacher = today_lessons_list[lesson_index]['object']
            else:
                if today_lessons_list[lesson_index]['teacher'] != '':
                    teacher = today_lessons_list[lesson_index]['teacher']
                else:
                    teacher = today_lessons_list[lesson_index]['replacement']
            teacher = teacher.replace(" (пог.)", "").replace("*", "").replace(".", "")
            room = today_lessons_list[lesson_index]['room']

            lesson = f'🕑 <b>{time}</b> | {room}\n' \
                     f'<i>{title}</i> ({lesson_type})\n' \
                     f'<pre>{teacher}</pre>\n'
            list_of_lessons.append(lesson)

    else:
        return None

    # glue all the lessons into one single message
    for each in list_of_lessons:
        message_of_lessons += each + '\n'

    message_of_lessons += schedule_statistics

    # return a single string of lessons
    return message_of_lessons
