from aiogram import Dispatcher, types

# from bot.handlers.menu import menu
from bot.keyboards.inline.settings_keyboard import get_settings_keyboard
from bot.keyboards.reply.menu_keyboard import menu_keyboard
from bot.states.UserStates import UserStates
from bot.storage.placeholders import messages
from loader import dp, bot


@dp.message_handler(state=UserStates.settings, commands=['settings'])
async def settings_handler(callback: types.CallbackQuery,):
    user = callback.from_user.id
    keyboard = get_settings_keyboard(user=user)
    await bot.send_message(chat_id=user, text=messages.SETTINGS_INFO, reply_markup=menu_keyboard)
    await bot.send_message(chat_id=user, text=messages.YOUR_SETTINGS, reply_markup=keyboard)


def register_settings_handler(dispatcher: Dispatcher):
    dispatcher.register_message_handler(settings_handler)
