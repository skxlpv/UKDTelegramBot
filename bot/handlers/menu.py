from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from bot.handlers.search import search_schedule
from bot.handlers.show_schedule import my_schedule
from bot.handlers.start import start
from bot.keyboards.reply.menu_keyboard import menu_keyboard
from bot.states.UserStates import UserStates
from loader import dp


@dp.message_handler(state=UserStates.menu)
async def menu(message: types.Message):
    await message.answer('Будь ласка, виберіть опцію', reply_markup=menu_keyboard)
    await UserStates.menu_handler.set()


@dp.message_handler(state=UserStates.menu_handler)
async def menu_handler(message: types.Message, state: FSMContext):
    if message.text == '/start':
        await start(message=message, state=state)

    if message.text == '/erase':
        await state.reset_state(with_data=True)
        await message.answer("Дані бота було стерто")

    if message.text == 'Знайти розклад':
        await UserStates.search.set()
        await search_schedule(message=message)

    elif message.text == 'Мій розклад':
        await my_schedule(message=message)

    elif message.text == 'Обране':
        await message.answer("Favorites is not implemented")


def register_menu_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(menu_handler)
