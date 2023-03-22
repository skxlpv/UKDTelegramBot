import requests

groups = requests.get('http://195.162.83.28/cgi-bin/timetable_export.cgi?req_type=obj_list&req_mode=group&show_ID=yes'
                      '&req_format=json&coding_mode=UTF8&bs=ok').json()
departments = groups['psrozklad_export']['departments'][0]['objects']
