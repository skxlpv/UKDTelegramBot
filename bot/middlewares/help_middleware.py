from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from bot.handlers.help import help_command


class HelpMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data):
        if message.text == '/help':
            await help_command(message=message)
