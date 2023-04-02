from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from bot.handlers.menu import menu
from bot.states.UserStates import UserStates
from loader import dp


@dp.message_handler(state='*', commands='restart')
async def restart_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.reset_state(with_data=True)
    await message.reply('Бот був перезавантажений.\nНадішліть /start для повторного запуску.',
                        reply_markup=types.ReplyKeyboardRemove())


def register_restart_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(restart_handler)
