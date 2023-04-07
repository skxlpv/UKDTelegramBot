import datetime

from aiogram import types, Bot
from aiogram.dispatcher import FSMContext

from bot.database.schedule_requests import get_from_collection, delete_favorite
from bot.handlers import menu
from bot.keyboards.inline.schedule_keyboard import get_schedule_keyboard
from bot.keyboards.reply.favorite_keyboard import favorite_keyboard
from bot.keyboards.reply.menu_keyboard import menu_keyboard
from bot.states.UserStates import UserStates
from bot.storage.placeholders import messages
from bot.utils.render_schedule import render_schedule
from bot.utils.search_utils import clear_keyboard
from configs import API_TOKEN
from loader import dp

bot = Bot(token=API_TOKEN)


@dp.message_handler(state=UserStates.show_favorites)
async def show_favorites(message: types.Message, state: FSMContext):
    favorites = get_from_collection(message.from_user.id, 'favorites')
    clear_keyboard(favorite_keyboard)
    if favorites not in (-20, -100, []):
        groups = []
        teachers = []
        for obj in favorites:
            if 'group_name' in obj:
                groups.append(obj['group_name'])
            elif 'teacher_name' in obj:
                teachers.append(obj['teacher_name'])
        for group in groups:
            favorite_keyboard.insert(group)
        for teacher in teachers:
            favorite_keyboard.insert(teacher)

        async with state.proxy() as state:
            state['favorites'] = favorites
        await message.answer(text=messages.SELECT_FROM_LIST, reply_markup=favorite_keyboard)
        await UserStates.get_favorite.set()
    else:
        await message.answer(text=messages.NOT_PICKED_ANY_GROUP, reply_markup=favorite_keyboard)
        await UserStates.menu.set()
        await menu.menu(message=message)


@dp.message_handler(state=UserStates.get_favorite)
async def get_favorite(message: types.Message, state: FSMContext):
    data = await state.get_data()
    favorites = data.get('favorites')
    found = False
    favorite = message.text
    for obj in favorites:
        if 'group_name' in obj and obj['group_name'] == favorite:
            found = True
            isTeacher = False
            group_id = obj['group_id']
            today_date = datetime.date.today().strftime("%d.%m.%Y")
            await state.reset_state()
            schedule = await render_schedule(search_name=message.text, search_id=group_id,
                                             begin_date=today_date, end_date=today_date,
                                             isTeacher=isTeacher, state=state)

            # if schedule validated (favorite exist)
            if await schedule_exist(user=message.from_user.id, group_id=group_id,
                                    isTeacher=isTeacher, schedule=schedule):
                await bot.send_message(chat_id=message.from_user.id, text='Ваш розклад:', reply_markup=menu_keyboard)
                keyboard = get_schedule_keyboard(user=message.from_user.id, group_id=group_id, isTeacher=isTeacher)
                await message.answer(schedule, parse_mode='HTML', reply_markup=keyboard)
                await UserStates.schedule_callback.set()

        elif 'teacher_name' in obj and obj['teacher_name'] == favorite:
            found = True
            isTeacher = True
            group_id = obj['teacher_id']
            await state.reset_state()
            today_date = datetime.date.today().strftime("%d.%m.%Y")
            schedule = await render_schedule(search_name=message.text, search_id=group_id,
                                             begin_date=today_date, end_date=today_date,
                                             isTeacher=isTeacher, state=state)

            # if schedule validated (favorite exist)
            if await schedule_exist(user=message.from_user.id, group_id=group_id,
                                    isTeacher=isTeacher, schedule=schedule):
                await bot.send_message(chat_id=message.from_user.id, text='Ваш розклад:', reply_markup=menu_keyboard)
                keyboard = get_schedule_keyboard(user=message.from_user.id, group_id=group_id, isTeacher=isTeacher)
                await message.answer(schedule, parse_mode='HTML', reply_markup=keyboard)
                await UserStates.schedule_callback.set()

    if not found:
        await UserStates.show_favorites.set()
        await message.answer(messages.SELECT_FROM_LIST, reply_markup=favorite_keyboard)


async def schedule_exist(user, isTeacher, group_id, schedule):
    if schedule in ('90',):
        await bot.send_message(chat_id=user,
                               text=messages.NOT_FOUND_OR_DELETED,
                               reply_markup=menu_keyboard)
        await UserStates.menu_handler.set()
        delete_favorite(user=user, group_id=group_id, isTeacher=isTeacher)
        return False
    return True
