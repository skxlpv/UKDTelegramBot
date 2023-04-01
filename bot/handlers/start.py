import logging

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from bot.handlers import menu
from loader import dp


@dp.message_handler(commands='erase', state='*')
async def erase(message: types.Message, state: FSMContext):
    await state.reset_state(with_data=True)
    await message.reply("Дані бота було стерто")


@dp.message_handler(commands='start', state='*')
async def start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(f'Вітаю, {message.from_user.first_name}!\n'
                         f'Я -- офіційний бот-асистент від Університету Короля Данила!\n')
    await menu.menu(message=message)


def register_start_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(start)
