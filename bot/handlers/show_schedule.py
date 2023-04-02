from datetime import datetime

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from bot.keyboards.inline.schedule_keyboard import schedule_keyboard
from bot.states.UserStates import UserStates
from bot.utils import schedule_utils
from loader import bot


async def my_schedule(message: types.Message, state: FSMContext, group_id, isTeacher, time_str=datetime.now().strftime('%d.%m.%Y')):
    final_string_of_lessons = schedule_utils.my_schedule_func(group_id=group_id, isTeacher=isTeacher, time_str=time_str)
    await bot.send_message(chat_id=message.from_user.id, text=f'{final_string_of_lessons}',
                           reply_markup=schedule_keyboard)
    async with state.proxy() as group:
        group['group_id'] = group_id
        group['isTeacher'] = isTeacher
    await UserStates.schedule_callback.set()


def register_schedule_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(my_schedule)

