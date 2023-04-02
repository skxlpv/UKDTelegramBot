from aiogram.dispatcher.middlewares import BaseMiddleware

from bot.handlers.menu import menu
from bot.handlers.restart import cancel_handler
from bot.states.UserStates import UserStates


class CancelMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message, data):
        if message.text == '/menu':
            await message.reply('Ми знову у головному меню!')
            await UserStates.menu.set()
