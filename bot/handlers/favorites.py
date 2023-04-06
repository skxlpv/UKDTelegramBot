import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.database.schedule_requests import get_from_collection
from bot.handlers import menu
from bot.keyboards.inline.schedule_keyboard import schedule_keyboard
from bot.keyboards.reply.favorite_keyboard import favorite_keyboard
from bot.states.UserStates import UserStates
from bot.utils.render_schedule import render_schedule
from bot.utils.search_utils import clear_keyboard
from loader import dp


@dp.message_handler(state=UserStates.show_favorites)
async def show_favorites(message: types.Message, state: FSMContext):
    favorites = get_from_collection(message.from_user.id, 'favorites')
    clear_keyboard(favorite_keyboard)
    if favorites not in (-20, -100):
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
        await message.answer('Виберіть зі списку:', reply_markup=favorite_keyboard)
        await UserStates.get_favorite.set()
    else:
        await message.answer('Вибачте, ви не обрали жодної групи', reply_markup=favorite_keyboard)
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
            await message.answer(schedule, parse_mode='HTML', reply_markup=schedule_keyboard)
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
            await message.answer(schedule, parse_mode='HTML', reply_markup=schedule_keyboard)
            await UserStates.schedule_callback.set()
    if not found:
        await UserStates.show_favorites.set()
        await message.answer('Виберіть зі списку:', reply_markup=favorite_keyboard)

