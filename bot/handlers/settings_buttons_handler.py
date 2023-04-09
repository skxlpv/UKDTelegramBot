from aiogram import types, Dispatcher

from bot.database.pref_requests import toggle_pref
from bot.keyboards.inline.settings_keyboard import get_settings_keyboard
from bot.states.UserStates import UserStates
from bot.storage.placeholders import callbacks
from loader import dp, bot


@dp.callback_query_handler(state=UserStates.settings)
async def callback_settings_buttons(callback: types.CallbackQuery):
    user = callback.from_user.id
    additional_courses = 'additional_courses'
    morning_schedule = 'morning_schedule'
    match callback.data:
        case str(additional_courses):
            toggle_pref(user=user, param=additional_courses)

        case morning_schedule:
            toggle_pref(user=user, param=morning_schedule)

    keyboard = get_settings_keyboard(user)
    await bot.edit_message_reply_markup(message_id=callback.message.message_id, chat_id=callback.from_user.id,
                                        reply_markup=keyboard)
    await callback.answer(text=callbacks.SETTINGS_CHANGED)


def register_schedule_answer_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(callback_settings_buttons)
