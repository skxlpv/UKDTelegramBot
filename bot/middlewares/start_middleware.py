from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from bot.handlers import start


class StartMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data):
        if message.text == '/start':
            await start.start(message=message, state=None)
