from aiogram import types, Dispatcher

from bot.handlers.menu import menu
from bot.states.UserStates import UserStates
from loader import dp

@dp.message_handler(commands=['start'], state=None)
async def start(message: types.Message):
    await message.answer(f'Вітаю, {message.from_user.first_name}!\n'
                         f'Я -- офіційний бот-асистент від Університету Короля Данила!\n')
    await UserStates.menu.set()
    await menu(message=message)


def register_start_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(start)
