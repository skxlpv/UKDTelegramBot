import typing

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from bot.handlers import menu
from bot.storage.placeholders import messages
from loader import dp


@dp.message_handler(commands='start', state='*')
async def start(message: types.Message, state: typing.Union[FSMContext, None]):
    if state:
        await state.finish()
    await message.answer(text=messages.WELCOME % message.from_user.first_name)
    await menu.menu(message=message)


def register_start_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(start)
