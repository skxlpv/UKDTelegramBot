from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from bot.states.UserStates import UserStates


class SettingsMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data):
        if message.text == '/settings':
            await UserStates.settings.set()
