import typing
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import BotCommand

from bot.handlers import menu
from loader import dp, bot


@dp.message_handler(commands='start', state='*')
async def start(message: types.Message, state: typing.Union[FSMContext, None]):
    if state:
        await state.finish()
    await message.answer(f'Вітаю, {message.from_user.first_name}!\n'
                         f'Я -- офіційний бот-асистент від Університету Короля Данила!\n')
    await menu.menu(message=message)


def register_start_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(start)
