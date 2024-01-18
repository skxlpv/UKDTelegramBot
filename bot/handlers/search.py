import datetime

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

import loader
from bot.keyboards.inline.role_keyboard import role_keyboard, degree_type_keyboard, institution_keyboard
from bot.keyboards.inline.schedule_keyboard import get_schedule_keyboard
from bot.keyboards.inline.search_keyboard import search_keyboard
from bot.keyboards.reply.course_keyboard import course_keyboard
from bot.keyboards.reply.group_keyboard import group_keyboard
from bot.keyboards.reply.menu_keyboard import menu_keyboard
from bot.keyboards.reply.specialties_keyboard import specialties_keyboard
from bot.keyboards.reply.teacher_keyboard import teacher_keyboard
from bot.states.UserStates import UserStates
from bot.storage.placeholders import messages
from bot.utils.api_requests import get_departments, get_teachers
from bot.utils.render_schedule import render_schedule
from bot.utils.search_utils import (insert_buttons, courses_list, groups_list,
                                    year_set, teacher_list,
                                    teacher_buttons_set, clear_keyboard, curr_year,
                                    specialities_dict)
from loader import dp, bot


# GENERAL SEARCH
@dp.message_handler(state=UserStates.search)
async def search_schedule(message: types.Message):
    await message.answer(text=messages.SEARCH_PARAMS, reply_markup=search_keyboard)
    await UserStates.search_options.set()


@dp.callback_query_handler(state=UserStates.search_options)
async def search_options(call: types.CallbackQuery, state: FSMContext):
    match call.data:
        case 'choice_search':
            await call.message.edit_text(text=messages.CHOOSE_ROLE, reply_markup=role_keyboard)
        case 'manual_search':
            await call.message.edit_text(text=messages.GROUP_FULL_NAME)
            await UserStates.manual_search.set()

        case 'student':
            await call.message.edit_text(text=messages.INSTITUTION_TYPE, reply_markup=institution_keyboard)

        case 'teacher':
            await call.message.delete()
            await call.message.answer(text=messages.TEACHER_INITIALS)
            await UserStates.search_teacher.set()

        case 'university':
            await call.message.edit_text(text=messages.DEGREE_TYPE, reply_markup=degree_type_keyboard)
            async with state.proxy() as data:
                data['institution'] = ''

        case 'college':
            await call.message.edit_text(text=messages.DEGREE_TYPE, reply_markup=degree_type_keyboard)
            async with state.proxy() as data:
                data['institution'] = 'К'

        case 'stationary':
            await call.message.delete()

            async with state.proxy() as data:
                data['degree_type'] = 'с'

            insert_buttons()
            await call.message.answer(text=messages.PICK_SPECIALITY, reply_markup=specialties_keyboard)
            await UserStates.get_specialty.set()

        case 'dual':
            await call.message.delete()

            async with state.proxy() as data:
                data['degree_type'] = 'д'

            insert_buttons()
            await call.message.answer(text=messages.PICK_SPECIALITY, reply_markup=specialties_keyboard)
            await UserStates.get_specialty.set()


# STUDENT GROUP SEARCH (by criteria)
@dp.message_handler(state=UserStates.get_specialty)
async def specialty_handler(message: types.Message, state: FSMContext):
    if message.text not in specialities_dict.values():
        await message.answer(text=messages.PICK_SPECIALITY_FAIL)
        await UserStates.get_specialty.set()
        loader.logger.error(f'User {message.from_user.id} failed to get specialty "{message.text}"')
    else:
        specialty = list(specialities_dict.keys())[list(specialities_dict.values()).index(message.text)]
        async with state.proxy() as data:
            data['specialty'] = data['institution'] + specialty + data['degree_type'] + '-'

        specialty = data.get('specialty')
        master_specialty = f'{specialty}'

        departments = get_departments()
        for index in range(len(departments)):
            group_name = departments[index]['name']
            if group_name.startswith(specialty) \
                    or group_name.startswith(master_specialty):
                edited_group = group_name.partition("-")[2]
                year = edited_group.partition('-')[0]
                year_set.add(year)

        years = sorted(list(year_set), reverse=True)

        for admission_year in years:
            current_year = curr_year
            admission_year = int(admission_year)

            # If current month is july or further
            if datetime.date.today().month >= 7:
                new_academic_year = 1
            else:
                new_academic_year = 0

            course = (current_year + new_academic_year) - admission_year
            course_keyboard.insert(messages.COURSE_NUM % course)
            courses_list.append(messages.COURSE_NUM % course)

        year_set.clear()
        clear_keyboard(specialties_keyboard)

        await message.answer(text=messages.COURSE_SELECT, reply_markup=course_keyboard)
        await UserStates.get_year.set()


@dp.message_handler(state=UserStates.get_year)
async def year_handler(message: types.Message, state: FSMContext):
    if message.text not in courses_list:
        await message.answer(text=messages.COURSE_SELECT_FAIL)
        await UserStates.get_year.set()
        loader.logger.error(f'User {message.from_user.id} failed to get year "{message.text}"')
    else:
        courses_list.clear()
        current_year = curr_year
        current_month = datetime.date.today().month
        year_of_admission = 0
        new_academic_year = 0

        # If current month is september or further
        if current_month >= 7:
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
        master_specialty_and_year = f'М{specialty_and_year}'

        clear_keyboard(course_keyboard)

        departments = get_departments()

        # Do NOT optimize it with 'in' in the future, because ІПЗс-21-2 in КІПЗс-21-2
        for index in range(len(departments)):
            group_name = departments[index]['name']
            if group_name.startswith(specialty_and_year) \
                    or group_name.startswith(master_specialty_and_year):
                group_keyboard.insert(group_name)
                groups_list.append(group_name)

        await message.answer(text=messages.GROUP_SELECT, reply_markup=group_keyboard)
        await UserStates.get_group.set()


@dp.message_handler(state=UserStates.get_group)
async def group_handler(message: types.Message, state: FSMContext):
    clear_keyboard(group_keyboard)
    if message.text not in groups_list:
        loader.logger.error(f'User {message.from_user.id} failed to get group "{message.text}"')
        await message.answer(text=messages.GROUP_SELECT_FAIL)
        await UserStates.get_group.set()

    else:
        groups_list.clear()
        group_name = message.text
        departments = get_departments()

        for index in range(len(departments)):
            if group_name == departments[index]['name']:
                group_id = departments[index]['ID']
                await group_search(group_id=group_id, message=message, group_name=group_name, state=state)
                await UserStates.schedule_callback.set()


# STUDENT GROUP SEARCH (by group title)
@dp.message_handler(state=UserStates.manual_search)
async def manual_search(message: types.Message, state: FSMContext):
    group_id = None
    group_name = message.text
    departments = get_departments()

    for index in range(len(departments)):
        if group_name.lower() == departments[index]['name'].lower():
            group_id = departments[index]['ID']
            await group_search(group_id=group_id, message=message, group_name=group_name, state=state)

    if group_id is None:
        loader.logger.info(f'User {message.from_user.id} not found group "{message.text}"')
        await message.answer(text=messages.GROUP_NOT_FOUND)


# TEACHER SCHEDULE SEARCH
@dp.message_handler(state=UserStates.search_teacher)
async def teacher_search(message: types.Message):
    received_teacher_name = message.text
    teachers = get_teachers()

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
        await message.answer(text=messages.TEACHER_SELECT, reply_markup=teacher_keyboard)
        await UserStates.get_teacher_schedule.set()
    else:
        loader.logger.info(f'User {message.from_user.id} not found teacher "{message.text}"')
        await message.answer(text=messages.TEACHER_INITIALS_FAIL)

    teacher_buttons_set.clear()
    clear_keyboard(teacher_keyboard)


@dp.message_handler(state=UserStates.get_teacher_schedule)
async def get_teacher_schedule(message: types.Message, state: FSMContext):
    teacher_id = None
    teacher_name = message.text
    teachers = get_teachers()

    for index in range(len(teachers)):
        all_teachers = teachers[index]['objects']
        for i in range(len(all_teachers)):
            teacher_object = teachers[index]['objects'][i]
            surname = teacher_object['P'].replace(" (пог.)", "").replace("*", "").replace(".", "")
            name = teacher_object['I']
            patronymic = teacher_object['B']

            if surname in teacher_name and name in teacher_name and patronymic in teacher_name:
                teacher_id = int(teacher_object['ID'])
                today_date = datetime.date.today().strftime("%d.%m.%Y")
                schedule = await render_schedule(search_name=teacher_name, search_id=teacher_id,
                                                 begin_date=today_date, end_date=today_date,
                                                 isTeacher=True, state=state,
                                                 user_id=message.from_user.id)
                await bot.send_message(chat_id=message.from_user.id, text=messages.YOUR_SCHEDULE, reply_markup=menu_keyboard)
                keyboard = get_schedule_keyboard(user=message.from_user.id, group_id=teacher_id, isTeacher=True)
                await message.answer(schedule, parse_mode='HTML', reply_markup=keyboard, disable_web_page_preview=True)
                await UserStates.schedule_callback.set()

    if teacher_id is None:
        loader.logger.info(f'User {message.from_user.id} not found teacher "{message.text}"')
        await message.answer(text=messages.TEACHER_NOT_FOUND)


async def group_search(group_id, message, group_name, state):
    today_date = datetime.date.today().strftime("%d.%m.%Y")
    schedule = await render_schedule(search_name=group_name, search_id=group_id,
                                     begin_date=today_date, end_date=today_date,
                                     isTeacher=False, state=state,
                                     user_id=message.from_user.id)
    await bot.send_message(chat_id=message.from_user.id, text=messages.YOUR_SCHEDULE, reply_markup=menu_keyboard)
    keyboard = get_schedule_keyboard(user=message.from_user.id, group_id=group_id, isTeacher=False)
    await message.answer(schedule, parse_mode='HTML', reply_markup=keyboard, disable_web_page_preview=True)
    await UserStates.schedule_callback.set()


def register_search_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(search_schedule)
    dispatcher.register_message_handler(manual_search)
