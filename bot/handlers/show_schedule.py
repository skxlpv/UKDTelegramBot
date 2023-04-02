from datetime import datetime

from aiogram import Dispatcher, types, Bot
from aiogram.dispatcher import FSMContext

from bot.database.schedule_requests import delete_favorite
from bot.keyboards.inline.schedule_keyboard import schedule_keyboard
from bot.keyboards.inline.yes_or_not_keyboard import tip_keyboard
from bot.keyboards.reply.menu_keyboard import menu_keyboard
from bot.states.UserStates import UserStates
from bot.utils import schedule_utils
from configs import API_TOKEN

bot = Bot(token=API_TOKEN)


async def my_schedule(user_id, state: FSMContext, group_id, isTeacher, time_str=datetime.now().strftime('%d.%m.%Y')):
    final_string_of_lessons = schedule_utils.my_schedule_func(group_id=group_id, isTeacher=isTeacher, time_str=time_str)
    if final_string_of_lessons == '90':
        await bot.send_message(chat_id=user_id,
                               text='Вибачте, даний розклад не знайдено чи було видалено',
                               reply_markup=menu_keyboard)
        await UserStates.menu_handler.set()
        delete_favorite(user=user_id, group_id=group_id, isTeacher=isTeacher)
    else:
        if final_string_of_lessons is None:
            final_string_of_lessons = 'Цього дня у вас немає пар. Відпочивайте!'
        await bot.send_message(chat_id=user_id, text=f'{final_string_of_lessons}',
                               reply_markup=schedule_keyboard)
        async with state.proxy() as group:
            group['group_id'] = group_id
            group['isTeacher'] = isTeacher
        await UserStates.schedule_callback.set()


def register_schedule_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(my_schedule)
