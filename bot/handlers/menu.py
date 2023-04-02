import requests
from datetime import datetime

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from bot.database.schedule_requests import get_from_collection
from bot.handlers import search
from bot.handlers.show_schedule import my_schedule
from bot.handlers.start import start
from bot.states.UserStates import UserStates

from bot.keyboards.reply.menu_keyboard import menu_keyboard
from bot.keyboards.inline.yes_or_not_keyboard import tip_keyboard

from loader import dp


@dp.message_handler(state=UserStates.menu)
async def menu(message: types.Message):
    await message.answer('Будь ласка, виберіть бажану опцію', reply_markup=menu_keyboard)
    await UserStates.menu_handler.set()


@dp.message_handler(state=UserStates.menu_handler)
async def menu_handler(message: types.Message, state: FSMContext):
    if message.text == '/start':
        await start(message=message, state=state)

    if message.text == 'Знайти розклад':
        await UserStates.search.set()
        await search.search_schedule(message=message)

    elif message.text == 'Мій розклад':
        primary = get_from_collection(message.from_user.id, 'primary')
        if primary != -20:
            time_str = datetime.now().strftime('%d.%m.%Y')
            if 'teacher_name' in primary:
                isTeacher = True
            else:
                isTeacher = False
            await my_schedule(message, state, primary['group_id'], time_str, isTeacher)
        else:
            await message.answer(text='От халепа! Схоже, ви ще не додали основний розклад! Підказати як це зробити?',
                                 reply_markup=tip_keyboard)
            await UserStates.tip_callback.set()
    elif message.text == 'Обране':
        await message.answer("Favorites is not implemented")


def register_menu_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(menu)
    dispatcher.register_message_handler(menu_handler)
