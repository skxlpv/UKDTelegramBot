from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from bot.states.UserStates import UserStates
from loader import dp, bot


@dp.message_handler(state='*', commands='cancel')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await UserStates.menu.set()
    await message.reply('Дія скасована.', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state='*', commands='restart')
async def restart_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.reset_state(with_data=True)
    await message.reply('Бот був перезавантажений.\nНадішліть /start для повторного запуску.',
                        reply_markup=types.ReplyKeyboardRemove())


def register_cancel_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(cancel_handler)
