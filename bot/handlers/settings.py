from aiogram import Dispatcher, types
from aiogram.types import ReplyKeyboardRemove

from bot.handlers.menu import menu
from bot.keyboards.inline.settings_keyboard import get_settings_keyboard
from bot.states.UserStates import UserStates
from loader import dp, bot


@dp.message_handler(state=UserStates.settings, commands=['settings'])
async def settings_handler(callback: types.CallbackQuery,):
    user = callback.from_user.id
    await bot.send_message(chat_id=user, text='Тут ви можете змінити ваші налаштування',
                           reply_markup=ReplyKeyboardRemove())
    keyboard = get_settings_keyboard(user=user)
    await bot.send_message(chat_id=user, text='Ваші поточні налаштування:', reply_markup=keyboard)
    match callback.data:
        case 'menu':
            await UserStates.menu.set()

def register_settings_handler(dispatcher: Dispatcher):
    dispatcher.register_message_handler(settings_handler)
