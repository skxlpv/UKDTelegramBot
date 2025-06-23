from datetime import datetime
import re

import requests
from aiogram.dispatcher import FSMContext

import loader
from bot.database.pref_requests import get_preferences
from bot.storage.placeholders import messages
from bot.utils.schedule_utils import day_of_week_dict, parse_text_or_link, parse_empty_tags


async def render_schedule(search_name, search_id, isTeacher, user_id, begin_date: datetime.date,
                          end_date: datetime.date, state: FSMContext):
    async with state.proxy() as data:  # put variables in storage
        data['search_name'] = search_name
        data['group_id'] = str(search_id)
        data['isTeacher'] = isTeacher

    schedule = get_schedule(search_name=search_name, search_id=search_id, isTeacher=isTeacher,
                            begin_date=begin_date, end_date=end_date, user_id=user_id)

    match schedule.replace('-', ''):
        case '1' | '4':
            schedule = messages.ERROR_NOT_EXIST
        case '90':
            schedule = messages.ERROR_OBJECT_NOT_EXIST
        case '2' | '3' | '6':
            schedule = messages.ERROR_BLOCKED

        case '60' | '70' | '80' | '100':
            schedule = messages.ERROR_ERROR

        case '200':
            schedule = messages.ERROR_SERVER

        case None:
            schedule = ''
            schedule += (messages.SEARCH_NAME % search_name)
            schedule += messages.NO_CLASSES

    return schedule


def get_schedule(search_name, search_id, isTeacher, user_id,
                 begin_date=None, end_date=None):
    if begin_date is None:
        begin_date = datetime.now().strftime('%d.%m.%Y')
    if end_date is None:
        end_date = datetime.now().strftime('%d.%m.%Y')
    list_of_lessons = []
    message_of_lessons = ''
    lessons_quantity = 0
    break_line = messages.BREAK_LINE
    # perform request based on isTeacher arg
    if isTeacher:
        request_mode = 'teacher'
    else:
        request_mode = 'group'

    try:
        response = requests.get(
            f'http://195.162.83.28/cgi-bin/timetable_export.cgi?req_type=rozklad&req_mode={request_mode}'
            f'&OBJ_ID={search_id}&OBJ_name=&dep_name=&ros_text=separated&begin_date={begin_date}&end_date={end_date}'
            f'&req_format=json&coding_mode=UTF8&bs=ok',
            timeout=5
        )

        if response.status_code != 200:
            loader.logging.error(f'Failed request: {response.status_code}')
            return f"Error: The request failed with status code {response.status_code}"

        obj = response.json()

        if 'error' in obj['psrozklad_export']:
            code = obj['psrozklad_export']['code']
            loader.logger.error(f'ERROR OCCURRED: {code}: User {user_id} tried to get data from API with '
                                f'search_id: {search_id}, search_name: {search_name} teacher: {isTeacher}, '
                                f'begin_date: {begin_date}, end_date: {end_date}')
            return code

    except requests.exceptions.Timeout:
        loader.logging.error(f"Request timed out for user {user_id}")
        return "Упс! Схоже, запит перевищив допустимий час обробки. Спробуйте ще раз згодом!"

    except requests.exceptions.RequestException as e:
        loader.logging.error(f"Request error occurred: {str(e)}")
        return "Упс. Схоже, виникла невідома помилка мережі. Спробуйте ще раз!"

    # generate group title
    today_lessons_list = obj['psrozklad_export']['roz_items']
    list_of_lessons.append(messages.SEARCH_NAME % search_name)

    # generate list of lessons
    if len(today_lessons_list) > 0:
        reservations_set = set()
        day_of_week = 0
        current_date = 0
        user_prefs = get_preferences(user_id)
        hasAdditionalCoursesOption = user_prefs['additional_courses']

        # get values
        for lesson_index in range(len(today_lessons_list)):
            object_date = today_lessons_list[lesson_index]['date']
            time = today_lessons_list[lesson_index]['lesson_time']
            title = today_lessons_list[lesson_index]['title']
            str_lesson_type = today_lessons_list[lesson_index]['type']
            str_half = today_lessons_list[lesson_index]['half']
            room = today_lessons_list[lesson_index]['room']
            comment4link = today_lessons_list[lesson_index]['comment4link']
            link = today_lessons_list[lesson_index]['link']
            online = today_lessons_list[lesson_index]['online']
            replacement = today_lessons_list[lesson_index]['replacement']
            reservation = today_lessons_list[lesson_index]['reservation']

            group = today_lessons_list[lesson_index]['group']
            teacher_current = today_lessons_list[lesson_index]['teacher']
            teacher_replacement = today_lessons_list[lesson_index]['replacement']

            if room == '' and online == 'Так':
                room = 'Онлайн'

            emoji = '🕑'

            lesson_type = f'({str_lesson_type})' if str_lesson_type != '' else str_lesson_type
            half = f'({str_half})' if str_half != '' else str_half

            if object_date != current_date:
                next_day_of_week = datetime.strptime(object_date, '%d.%m.%Y').weekday()
                list_of_lessons.append(break_line)
                list_of_lessons.append(messages.DAY_AND_DATE % (f'📆 {day_of_week_dict[next_day_of_week]}',
                                                                f'{object_date}\n'))
                current_date = object_date
                day_of_week += next_day_of_week

            if 'ПК' in group or 'Складання' in reservation:
                if hasAdditionalCoursesOption:
                    emoji = '🌀'
                else:
                    continue

            if isTeacher:
                teacher = group
            else:
                teacher = teacher_current if teacher_current != '' else teacher_replacement

            teacher = teacher.replace(" (пог.)", "").replace("*", "").replace(".", "")

            tags = re.findall('(<.*?>)', title)

            for tag in tags:
                title = title.replace(tag, '')

            if replacement != '':
                replacement = f'⚠️ {replacement} ⚠️'

            if reservation and title == '':
                pattern = re.compile(r'<.*?>')
                reservation = re.sub(pattern, '', reservation)
                if reservation not in reservations_set:
                    reservations_set.add(reservation)
                    title = reservation + '\n'
                    time = 'УВЕСЬ ДЕНЬ'
                else:
                    continue

            lesson = messages.LESSON % (emoji, time, room, title, lesson_type, half, teacher, replacement)

            lesson = parse_empty_tags(lesson) + '\n'

            _comment, _link = parse_text_or_link(comment4link)

            if comment4link == '' and link == '':
                pass
            elif comment4link == '':
                lesson += f'{link}\n'
            elif link == '':
                if _comment != '':
                    if _link != '':
                        lesson += f'<a href="{_link}">{_comment}</a>'
                    else:
                        lesson += f'{_comment}\n'
            else:
                lesson += f'\n{_comment}\n' \
                          f'{link}\n'

            list_of_lessons.append(lesson)
            lessons_quantity += 1

    else:
        return None

    if lessons_quantity == 0:
        return None

    # glue all the lessons into one single message
    for each in list_of_lessons:
        message_of_lessons += each + '\n'
        message_of_lessons.strip()

    message_of_lessons += messages.CLASSES_QUANTITY % lessons_quantity

    # return a single string of lessons
    loader.logger.info(f'User {user_id} got data from API with search_id: {search_id}, '
                       f'search_name: {search_name} teacher: {isTeacher}, '
                       f'begin_date: {begin_date}, end_date: {end_date}')
    return message_of_lessons
