from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from bot.states.UserStates import UserStates


class MenuMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data):
        if message.text == '/menu':
            await message.reply('<em><strong>Головне меню!</strong></em>',
                                parse_mode='HTML')
            await UserStates.menu.set()
