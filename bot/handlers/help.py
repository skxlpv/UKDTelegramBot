from aiogram import types, Dispatcher

from bot.handlers import menu
from bot.storage.placeholders import messages
from loader import dp


@dp.message_handler(commands='help', state='*')
async def help_command(message: types.Message):
    await message.answer(text=messages.HELP, parse_mode='HTML')
    await menu.menu(message=message)


def register_help_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(help_command)
