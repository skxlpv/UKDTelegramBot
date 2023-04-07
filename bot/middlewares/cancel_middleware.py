from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from bot.states.UserStates import UserStates
from bot.storage.placeholders import messages


class CancelMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data):
        if message.text == '/cancel':
            await message.reply(text=messages.MENU,
                                parse_mode='HTML')
            await UserStates.menu.set()
