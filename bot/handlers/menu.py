from aiogram import types, Dispatcher

from bot.handlers import search, favorites
from bot.handlers.show_schedule import my_schedule
from bot.keyboards.reply.menu_keyboard import menu_keyboard
from bot.states.UserStates import UserStates
from loader import dp


@dp.message_handler(state=UserStates.menu)
async def menu(message: types.Message):
    await message.answer('Будь ласка, виберіть бажану опцію', reply_markup=menu_keyboard)
    await UserStates.menu_handler.set()


@dp.message_handler(state=UserStates.menu_handler)
async def menu_handler(message: types.Message):
    if message.text == 'Знайти розклад':
        await UserStates.search.set()
        await search.search_schedule(message=message)

    elif message.text == 'Мій розклад':
        await my_schedule(message=message)

    elif message.text == 'Обране':
        await UserStates.get_favorites.set()
        await favorites.show_favorites(message=message)
        # await message.answer("Favorites is not implemented")


def register_menu_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(menu)
    dispatcher.register_message_handler(menu_handler)
