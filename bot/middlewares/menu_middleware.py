from aiogram.dispatcher.middlewares import BaseMiddleware

from bot.states.UserStates import UserStates


class MenuMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message, data):
        if message.text == '/menu':
            await message.reply('Ми знову у головному меню!')
            await UserStates.menu.set()
