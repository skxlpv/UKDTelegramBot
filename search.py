# Проблема в кнопках в обох методах, фіксити
# Проблема в кнопках в обох методах, фіксити
# Проблема в кнопках в обох методах, фіксити

import json
import logging
import re
from urllib import parse
from main import API_TOKEN
import datetime

import requests
from aiogram import Bot, Dispatcher, executor, types

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import aiogram.utils.markdown as md
from aiogram.types import ParseMode


from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

#############################   API GET CALL   ##################################
response = requests.get('http://195.162.83.28/cgi-bin/timetable_export.cgi?req_type=obj_list&req_mode=group&show_ID=yes&req_format=json&coding_mode=UTF8&bs=ok')
obj = response.json()
departments = obj['psrozklad_export']['departments'][0]['objects']
#################################################################################

API_TOKEN = API_TOKEN

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)

# Global Variables

#////////////////////////////////////  MAIN CODE   ////////////////////////////////////
list_of_specialties = []
def get_departments():
    for each in range(len(departments)):
            department = departments[each]['name']
            list_of_specialties.append(department)
    return list_of_specialties

class UserStates(StatesGroup):
    specialty = State()
    year = State()
    group = State()


buttonChoiceSearch = InlineKeyboardButton(text='За критеріями', callback_data='choiceSearch')
buttonManualSearch = InlineKeyboardButton(text='За назвою', callback_data='manualSearch')
searchKeyboard = InlineKeyboardMarkup().add(buttonChoiceSearch, buttonManualSearch)

buttonRoleStudent = InlineKeyboardButton(text='Студент/ка', callback_data='student')
buttonRoleTeacher = InlineKeyboardButton(text='Викладач/ка', callback_data='teacher')
roleKeyboard = InlineKeyboardMarkup().add(
    buttonRoleStudent, buttonRoleTeacher
)

listOfCourses = {
    '1': '1 курс', 
    '2': '2 курс', 
    '3': '3 курс', 
    '4': '4 курс'
}

listOfGroups = {
    '1': '1 група', 
    '2': '2 група', 
    '3': '3 група', 
    'None': 'Відсутня'
}


buttonFirstCourse = KeyboardButton(listOfCourses['1'])
buttonSecondCourse = KeyboardButton(listOfCourses['2'])
buttonThirdCourse = KeyboardButton(listOfCourses['3'])
buttonFourthCourse = KeyboardButton(listOfCourses['4'])
courseKeyboard = ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)

buttonFirstGroup = KeyboardButton(listOfGroups['1'])
buttonSecondGroup = KeyboardButton(listOfGroups['2'])
buttonThirdGroup = KeyboardButton(listOfGroups['3'])
buttonNoneGroup = KeyboardButton(listOfGroups['None'])

groupKeyboard = ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)

specialtyKeyboard = ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)

def get_buttons():
    buttons_set = set()
    for value in range(len(departments)):
        group_name = departments[value]['name']
        button_title = "".join([ch for ch in group_name if ch.isalpha()])

        if button_title.endswith('с') or button_title.endswith('д') or button_title.endswith('з'):
            button_title = button_title[:-1]

        buttons_set.add(button_title)
    return(sorted(buttons_set))

def insert_buttons(buttons_set=get_buttons()):
    for each in buttons_set:
        specialtyKeyboard.insert(each)

specialtiesList = list(get_buttons())

list_of_stationary = []

def get_stationary():
    for value in range(len(departments)):
        group = departments[value]['name']
        title = "".join([ch for ch in group if ch.isalpha()])

        if title.endswith('с'):
            list_of_stationary.append(group)

    return list_of_stationary


@dp.message_handler(commands=['search'])
async def search_schedule(message: types.Message):
    await message.answer('Оберіть параметри пошуку', reply_markup=searchKeyboard)


@dp.callback_query_handler(text = ['choiceSearch', 'student'])
async def callback_handler(call: types.CallbackQuery):
    if call.data == 'choiceSearch':
        await call.message.edit_text('Вкажіть роль', reply_markup=roleKeyboard)

    if call.data == 'student':
        insert_buttons()
        await UserStates.specialty.set()

        await call.message.delete()
        await call.message.answer('Оберіть спеціальність', reply_markup=specialtyKeyboard)
            

year_set = set()
courses_list = []
groups_list = []
@dp.message_handler(state=UserStates.specialty, text = specialtiesList)
async def specialty_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['specialty'] = message.text + 'с' + '-'

    for group in get_stationary():
        if message.text in group:
            edited_group = group.partition("-")[2]
            year = edited_group.partition('-')[0]
            year_set.add(year)
    
    years = sorted(list(year_set), reverse=True)

    for admission_year in years:
        current = datetime.date.today().year - 2000
        admission_year = int(admission_year)
        if datetime.date.today().month >= 9: 
            new_academic_year = 1
        else: new_academic_year = 0
        course = (current + new_academic_year) - admission_year
        courseKeyboard.insert(f'{course} курс')
        courses_list.append(f'{course} курс')
    
    year_set.clear()

    await UserStates.next()

    for key, value in specialtyKeyboard.values.copy().items():
        if key == 'keyboard':
            specialtyKeyboard.values[key].clear()

    await message.answer('Оберіть курс', reply_markup=courseKeyboard)
    

@dp.message_handler(state=UserStates.year, text = courses_list)
async def specialty_handler(message: types.Message, state: FSMContext):
    courses_list.clear()
    current_year = datetime.date.today().year - 2000 # Keep only tens
    current_month = datetime.date.today().month
    year_of_admission = 0

    if current_month >= 9: # If current month is semptember or further
        if message.text == listOfCourses['1']:
            year_of_admission = (current_year+1) - 1
        elif message.text == listOfCourses['2']:
            year_of_admission = (current_year + 1) - 2
        elif message.text == listOfCourses['3']:
            year_of_admission = (current_year + 1) - 3
        elif message.text == listOfCourses['4']:
            year_of_admission = (current_year + 1) - 4

    elif current_month < 9: # If current month is not semptember or less
        if message.text == listOfCourses['1']:
            year_of_admission = current_year - 1
        elif message.text == listOfCourses['2']:
            year_of_admission = current_year - 2
        elif message.text == listOfCourses['3']:
            year_of_admission = current_year - 3
        elif message.text == listOfCourses['4']:
            year_of_admission = current_year - 4

    async with state.proxy() as data:
        data['year'] = str(year_of_admission)
    
    specialty_and_year = data['specialty'] + data['year']


    for key, value in courseKeyboard.values.copy().items():
        if key == 'keyboard':
            courseKeyboard.values[key].clear()



    for index in range(len(departments)):
        if specialty_and_year in departments[index]['name']:
            groupKeyboard.insert(departments[index]['name'])
            groups_list.append(departments[index]['name'])

    await message.answer('Оберіть групу', reply_markup=groupKeyboard)
    await UserStates.next()
    


@dp.message_handler(state=UserStates.group, text = groups_list)
async def get_group(message: types.Message, state: FSMContext):
    groups_list.clear()
    await state.reset_state(with_data=False)

    for key, value in groupKeyboard.values.copy().items():
        if key == 'keyboard':
            groupKeyboard.values[key].clear()

    group = message.text
    for index in range(len(departments)):
        if group == departments[index]['name']:
            group_id = departments[index]['ID']

            response = requests.get(f'http://195.162.83.28/cgi-bin/timetable_export.cgi?req_type=rozklad&req_mode=group&OBJ_ID={group_id}&OBJ_name=&dep_name=&ros_text=separated&show_empty=yes&begin_date=&end_date=&req_format=json&coding_mode=UTF8&bs=ok').json()
            return await message.answer(response, reply_markup=ReplyKeyboardRemove())
    
@dp.message_handler(state='*')
async def message_handler(message: types.Message, state: FSMContext):
    current = await state.get_state()
    # if current is None:
    #     return
    
    if message.text and current is None:
        await message.answer('Не зрозумів вас! Будь ласка, повторіть спробу.')

    if current is not None and message.text and UserStates.specialty._state in current:
        await message.answer('Будь ласка, оберіть спеціальність!')
    
    if current is not None and message.text and UserStates.year._state in current:
        await message.answer('Будь ласка, оберіть курс!')

    if current is not None and message.text and UserStates.group._state in current:
        await message.answer('Будь ласка, оберіть групу!')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)