from aiogram import Dispatcher, types

from bot.states.UserStates import UserStates
from loader import dp


@dp.message_handler(state=UserStates.settings)
async def settings_handler(message: types.Message):
    await message.answer('HERE GO SETTINGS!')


def register_settings_handler(dispatcher: Dispatcher):
    dispatcher.register_message_handler(settings_handler)