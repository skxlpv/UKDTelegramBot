import datetime
import requests

from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext

from bot.handlers.menu import menu
from bot.states.UserStates import UserStates
from loader import dp
from bot.keyboards.inline.role_keyboard import role_keyboard
from bot.keyboards.inline.search_keyboard import search_keyboard
from bot.keyboards.reply.specialties_keyboard import specialties_keyboard
from bot.keyboards.reply.course_keyboard import course_keyboard
from bot.keyboards.reply.group_keyboard import group_keyboard
from bot.utils.search_utils import (insert_buttons, courses_list, groups_list,
                                    year_set, shrinked_specialties_list, get_stationary,
                                    list_of_courses)
from bot.utils.api_requests import departments


@dp.message_handler(state=UserStates.search)
async def search_schedule(message: types.Message):
    await message.answer('Оберіть параметри пошуку', reply_markup=search_keyboard)
    await UserStates.search_options.set()


@dp.callback_query_handler(state=UserStates.search_options)
async def search_options(call: types.CallbackQuery):
    if call.data == 'choice_search':
        await call.message.edit_text('Вкажіть роль', reply_markup=role_keyboard)

    if call.data == 'manual_search':
        await call.message.edit_text('Надішліть повну назву шуканої групи')
        await UserStates.manual_search.set()

    if call.data == 'student':
        await call.message.delete()

        insert_buttons()
        await call.message.answer('Оберіть спеціальність', reply_markup=specialties_keyboard)
        await UserStates.get_specialty.set()


@dp.message_handler(state=UserStates.get_specialty)
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

        # If current month is semptember or further
        if datetime.date.today().month >= 9:
            new_academic_year = 1
        else:
            new_academic_year = 0

        course = (current + new_academic_year) - admission_year
        course_keyboard.insert(f'{course} курс')
        courses_list.append(f'{course} курс')

    year_set.clear()

    for key, value in specialties_keyboard.values.copy().items():
        if key == 'keyboard':
            specialties_keyboard.values[key].clear()

    await message.answer('Оберіть курс', reply_markup=course_keyboard)
    await UserStates.get_year.set()


@dp.message_handler(state=UserStates.get_year)
async def year_handler(message: types.Message, state: FSMContext):
    courses_list.clear()
    current_year = datetime.date.today().year - 2000  # Keep only tens
    current_month = datetime.date.today().month
    year_of_admission = 0

    # If current month is september or further
    if current_month >= 9:
        new_academic_year = 1
    elif current_month < 9:
        new_academic_year = 0

    if message.text == list_of_courses['1']:
        year_of_admission = (current_year + new_academic_year) - 1
    elif message.text == list_of_courses['2']:
        year_of_admission = (current_year + new_academic_year) - 2
    elif message.text == list_of_courses['3']:
        year_of_admission = (current_year + new_academic_year) - 3
    elif message.text == list_of_courses['4']:
        year_of_admission = (current_year + new_academic_year) - 4

    async with state.proxy() as data:
        data['year'] = str(year_of_admission)

    specialty_and_year = data['specialty'] + data['year']

    for key, value in course_keyboard.values.copy().items():
        if key == 'keyboard':
            course_keyboard.values[key].clear()

    for index in range(len(departments)):
        if specialty_and_year in departments[index]['name']:
            group_keyboard.insert(departments[index]['name'])
            groups_list.append(departments[index]['name'])

    await message.answer('Оберіть групу', reply_markup=group_keyboard)
    await UserStates.get_group.set()


@dp.message_handler(state=UserStates.get_group)
async def group_handler(message: types.Message):
    groups_list.clear()

    for key, value in group_keyboard.values.copy().items():
        if key == 'keyboard':
            group_keyboard.values[key].clear()

    group = message.text

    for index in range(len(departments)):
        if group == departments[index]['name']:
            group_id = departments[index]['ID']

            response = requests.get(
                f'http://195.162.83.28/cgi-bin/timetable_export.cgi?req_type=rozklad&req_mode=group&OBJ_ID={group_id}&OBJ_name=&dep_name=&ros_text=separated&show_empty=yes&begin_date=24.03.23&end_date=24.03.23&req_format=json&coding_mode=UTF8&bs=ok'
            ).json()
            await message.answer(response, reply_markup=ReplyKeyboardRemove())

    await UserStates.menu.set()
    await menu(message=message)


# ////////////////////////////////////////////////////////////////////////////
@dp.message_handler(state=UserStates.manual_search)
async def manual_search(message: types.Message, state: FSMContext):
    group_id = None
    group_title = message.text
    for index in range(len(departments)):
        if group_title.lower() == departments[index]['name'].lower():
            group_id = departments[index]['ID']

            response = requests.get(
                f'http://195.162.83.28/cgi-bin/timetable_export.cgi?req_type=rozklad&req_mode=group&OBJ_ID={group_id}&OBJ_name=&dep_name=&ros_text=separated&show_empty=yes&begin_date=24.03.23&end_date=24.03.23&req_format=json&coding_mode=UTF8&bs=ok'
            ).json()
            await message.answer(response, reply_markup=ReplyKeyboardRemove())
            await UserStates.menu.set()
            await menu(message=message)

    if group_id is None:
        await message.answer('Групу не знайдено! Спробуйте ще раз!')


def register_search_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(search_schedule)
    dispatcher.register_message_handler(manual_search)
    dispatcher.register_callback_query_handler(search_options)
    dispatcher.register_message_handler(specialty_handler)
    dispatcher.register_message_handler(year_handler)
    dispatcher.register_message_handler(group_handler)
