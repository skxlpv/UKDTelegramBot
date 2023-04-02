from datetime import datetime, timedelta

import requests


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


def remove_last_line_from_string(final_string_of_lessons):
    return final_string_of_lessons[:final_string_of_lessons.rfind('\n- - - - - - - - -')]
