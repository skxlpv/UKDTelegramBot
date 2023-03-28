
from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext

from bot.database.schedule_requests import get_from_collection
from bot.utils.search_utils import clear_keyboard
from loader import dp
from bot.states.UserStates import UserStates

from bot.keyboards.reply.favorite_keyboard import favorite_keyboard


@dp.message_handler(state=UserStates.get_favorites)
async def show_favorites(message: types.Message):
    favorites = get_from_collection(message.from_user.id, 'favorites')
    clear_keyboard(favorite_keyboard)
    if favorites not in (-20, -100):
        for obj in favorites:
            favorite_keyboard.insert(obj['group_name'])
        await UserStates.manual_search.set()
        await message.answer('Виберіть групу зі списку:', reply_markup=favorite_keyboard)
    else:
        await message.answer('Вибачте, ви не обрали жодної групи', reply_markup=favorite_keyboard)
        await UserStates.menu.set()
