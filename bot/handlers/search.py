import datetime
import requests
import time

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from bot.handlers.show_schedule import my_schedule
from bot.keyboards.reply.teacher_keyboard import teacher_keyboard
from bot.states.UserStates import UserStates
from loader import dp
from bot.keyboards.inline.role_keyboard import role_keyboard
from bot.keyboards.inline.search_keyboard import search_keyboard
from bot.keyboards.reply.specialties_keyboard import specialties_keyboard
from bot.keyboards.reply.course_keyboard import course_keyboard
from bot.keyboards.reply.group_keyboard import group_keyboard
from bot.utils.search_utils import (insert_buttons, courses_list, groups_list,
                                    year_set, get_stationary, teacher_list,
                                    teacher_buttons_set, clear_keyboard, curr_year, shrinked_specialties_list)
from bot.utils.api_requests import departments, teachers


# GENERAL SEARCH
@dp.message_handler(state=UserStates.search)
async def search_schedule(message: types.Message):
    await message.answer('Оберіть параметри пошуку розкладу', reply_markup=search_keyboard)
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

    if call.data == 'teacher':
        await call.message.delete()
        await call.message.answer("Введіть П.І.Б.")
        await UserStates.search_teacher.set()


# STUDENT GROUP SEARCH (by criteria)
@dp.message_handler(state=UserStates.get_specialty)
async def specialty_handler(message: types.Message, state: FSMContext):
    if message.text not in shrinked_specialties_list:
        await message.answer('Будь ласка, оберіть спеціальність')
        await UserStates.get_specialty.set()

    else:
        async with state.proxy() as data:
            data['specialty'] = message.text + 'с' + '-'

        for group in get_stationary():
            if message.text in group:
                edited_group = group.partition("-")[2]
                year = edited_group.partition('-')[0]
                year_set.add(year)

        years = sorted(list(year_set), reverse=True)

        for admission_year in years:
            current_year = curr_year
            admission_year = int(admission_year)

            # If current month is september or further
            if datetime.date.today().month >= 9:
                new_academic_year = 1
            else:
                new_academic_year = 0

            course = (current_year + new_academic_year) - admission_year
            course_keyboard.insert(f'{course} курс')
            courses_list.append(f'{course} курс')

        year_set.clear()
        clear_keyboard(specialties_keyboard)

        await message.answer('Оберіть курс', reply_markup=course_keyboard)
        await UserStates.get_year.set()


@dp.message_handler(state=UserStates.get_year)
async def year_handler(message: types.Message, state: FSMContext):
    if message.text not in courses_list:
        await message.answer('Будь ласка, оберіть курс')
        await UserStates.get_year.set()

    else:
        courses_list.clear()
        current_year = curr_year
        current_month = datetime.date.today().month
        year_of_admission = 0
        new_academic_year = 0

        # If current month is september or further
        if current_month >= 9:
            new_academic_year = 1

        match message.text:
            case "1 курс":
                year_of_admission = (current_year + new_academic_year) - 1
            case "2 курс":
                year_of_admission = (current_year + new_academic_year) - 2
            case "3 курс":
                year_of_admission = (current_year + new_academic_year) - 3
            case "4 курс":
                year_of_admission = (current_year + new_academic_year) - 4

        async with state.proxy() as data:
            data['year'] = str(year_of_admission)

        specialty_and_year = data['specialty'] + data['year']

        clear_keyboard(course_keyboard)

        for index in range(len(departments)):
            if specialty_and_year in departments[index]['name']:
                group_keyboard.insert(departments[index]['name'])
                groups_list.append(departments[index]['name'])

        await message.answer('Оберіть групу', reply_markup=group_keyboard)
        await UserStates.get_group.set()


@dp.message_handler(state=UserStates.get_group)
async def group_handler(message: types.Message, state: FSMContext):
    clear_keyboard(group_keyboard)
    if message.text not in groups_list:
        await message.answer('Будь ласка, оберіть групу')
        await UserStates.get_group.set()

    else:
        groups_list.clear()
        group = message.text

        for index in range(len(departments)):
            if group == departments[index]['name']:
                group_id = departments[index]['ID']

                time_str = time.strftime("%d.%m.%Y")

                data = requests.get(
                    f'http://195.162.83.28/cgi-bin/timetable_export.cgi?req_type=rozklad&req_mode=group&OBJ_ID={group_id}'
                    f'&OBJ_name=&dep_name=&ros_text=separated&show_empty=yes&begin_date={time_str}&end_date={time_str}&req_'
                    f'format=json&coding_mode=UTF8&bs=ok'
                ).json()
                # async with state.proxy() as response:
                #     response['data'] = data
                # set_primary(user=message.from_user.id,  group_id=group_id, )
                await my_schedule(message, state, group_id, time_str, isTeacher=False)
                # await message.answer(response, reply_markup=ReplyKeyboardRemove())

            # await UserStates.menu.set()
            # await menu(message=message)


# STUDENT GROUP SEARCH (by group title)
@dp.message_handler(state=UserStates.manual_search)
async def manual_search(message: types.Message, state: FSMContext):
    group_id = None
    group_title = message.text
    for index in range(len(departments)):
        if group_title.lower() == departments[index]['name'].lower():
            group_id = departments[index]['ID']

            time_str = time.strftime("%d.%m.%Y")

            data = requests.get(
                f'http://195.162.83.28/cgi-bin/timetable_export.cgi?req_type=rozklad&req_mode=group&OBJ_ID={group_id}'
                f'&OBJ_name=&dep_name=&ros_text=separated&show_empty=yes&begin_date={time_str}&end_date={time_str}&'
                f'req_format=json&coding_mode=UTF8&bs=ok'
            ).json()

            await my_schedule(message, state, group_id, time_str, isTeacher=False)
            # async with state.proxy() as response:
            #     response['data'] = data
            # await my_schedule(message, state)
            # await message.answer(response, reply_markup=ReplyKeyboardRemove())
            # await UserStates.menu.set()
            # await menu(message=message)

    if group_id is None:
        await message.answer('Групу не знайдено! Спробуйте ще раз!')


# TEACHER SCHEDULE SEARCH
@dp.message_handler(state=UserStates.search_teacher)
async def teacher_search(message: types.Message):
    received_teacher_name = message.text

    for index in range(len(teachers)):
        all_teachers = teachers[index]['objects']
        for i in range(len(all_teachers)):
            teacher_object = teachers[index]['objects'][i]
            teacher_name = teacher_object['P'] + ' ' + teacher_object['I'] + ' ' + teacher_object['B']
            teacher_name = teacher_name.replace(" (пог.)", "").replace("*", "").replace(".", "")
            teacher_list.append(teacher_name)

    for name in teacher_list:
        if received_teacher_name.lower() in name.lower():
            teacher_buttons_set.add(name)

    for name in teacher_buttons_set:
        teacher_keyboard.add(name)

    if len(teacher_buttons_set) > 0:
        await message.answer("Оберіть викладача із запропонованих", reply_markup=teacher_keyboard)
        await UserStates.get_teacher_schedule.set()
    else:
        await message.answer("Будь ласка, введіть П.І.Б. викладача")

    teacher_buttons_set.clear()
    clear_keyboard(teacher_keyboard)


@dp.message_handler(state=UserStates.get_teacher_schedule)
async def get_teacher_schedule(message: types.Message, state: FSMContext):
    t_id = None
    t_name = message.text

    for index in range(len(teachers)):
        all_teachers = teachers[index]['objects']
        for i in range(len(all_teachers)):
            t = teachers[index]['objects'][i]
            surname = t['P'].replace(" (пог.)", "").replace("*", "").replace(".", "")
            name = t['I']
            patronymic = t['B']

            if surname in t_name and name in t_name and patronymic in t_name:
                t_id = int(t['ID'])
                time_str = time.strftime("%d.%m.%Y")

                response = requests.get(
                    f'http://195.162.83.28/cgi-bin/timetable_export.cgi?req_type=rozklad&req_mode=teacher&OBJ_ID={t_id}'
                    '&OBJ_name=&dep_name=&ros_text=separated&begin_date=27.03.23&end_date=27.03.23&req_format=json'
                    '&coding_mode=UTF8&bs=ok'
                ).json()
                await my_schedule(message, state, t_id, time_str, isTeacher=True)

    if t_id is None:
        await message.answer('Вчителя не знайдено! Спробуйте ще раз!')

    # await UserStates.menu.set()
    # await menu(message=message)


def register_search_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(search_schedule)
    dispatcher.register_message_handler(manual_search)
