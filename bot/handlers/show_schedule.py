from aiogram import Dispatcher, types
import requests

from aiogram.dispatcher import FSMContext
from loader import dp
from loader import bot

from bot.keyboards.inline.schedule_keyboard import schedule_keyboard
from bot.utils import schedule_utils
from bot.states.UserStates import UserStates


async def my_schedule(message: types.Message, state: FSMContext, group_id, time_str, student):
    final_string_of_lessons = schedule_utils.my_schedule_func(group_id, time_str, student)
    await bot.send_message(chat_id=message.from_user.id, text=f'f3ogiog4jg\n—————\n{final_string_of_lessons}',
                           reply_markup=schedule_keyboard)
    async with state.proxy() as group:
        group['group_id'] = group_id
        group['student'] = student
    await UserStates.schedule_callback.set()


def register_schedule_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(my_schedule)

