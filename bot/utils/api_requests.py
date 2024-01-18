import requests


def get_departments():
    departments_data = requests.get(
        'http://195.162.83.28/cgi-bin/timetable_export.cgi?req_type=obj_list&req_mode=group&show_ID=yes'
        '&req_format=json&coding_mode=UTF8&bs=ok').json()

    departments = departments_data['psrozklad_export']['departments'][0]['objects']
    departments += (departments_data['psrozklad_export']['departments'][1]['objects'])
    return departments


def get_teachers():
    teachers_data = requests.get(
        'http://195.162.83.28/cgi-bin/timetable_export.cgi?req_type=obj_list&req_mode=teacher&show_ID'
        '=yes&req_format=json&coding_mode=UTF8&bs=ok').json()
    teachers = teachers_data['psrozklad_export']['departments']
    return teachers
