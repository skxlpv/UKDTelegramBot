from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from bot.database.schedule_requests import get_from_collection
from bot.handlers import search, favorites
from bot.handlers.show_schedule import my_schedule
from bot.keyboards.inline.yes_or_not_keyboard import tip_keyboard
from bot.keyboards.reply.menu_keyboard import menu_keyboard
from bot.states.UserStates import UserStates
from loader import dp


@dp.message_handler(state=UserStates.menu)
async def menu(message: types.Message):
    await message.answer('Будь ласка, виберіть бажану опцію', reply_markup=menu_keyboard)
    await UserStates.menu_handler.set()


@dp.message_handler(state=UserStates.menu_handler)
async def menu_handler(message: types.Message, state:FSMContext):
    if message.text == 'Знайти розклад':
        await UserStates.search.set()
        await search.search_schedule(message=message)

    elif message.text == 'Мій розклад':
        primary = get_from_collection(message.from_user.id, 'primary')
        if primary != -20:
            if 'teacher_name' in primary:
                isTeacher = True
                group_id = primary['teacher_id']
            else:
                isTeacher = False
                group_id = primary['group_id']
            await my_schedule(user_id=message.from_user.id, state=state, group_id=group_id, isTeacher=isTeacher)
        else:
            await message.answer(text='От халепа! Схоже, ви ще не додали основний розклад! Підказати як це зробити?',
                                 reply_markup=tip_keyboard)
            await UserStates.tip_callback.set()
    elif message.text == 'Обране':
        await UserStates.show_favorites.set()
        await favorites.show_favorites(message=message, state=state)


def register_menu_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(menu)
    dispatcher.register_message_handler(menu_handler)
