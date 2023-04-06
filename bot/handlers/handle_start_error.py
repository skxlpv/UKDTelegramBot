from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from loader import dp


@dp.message_handler(state='*')
async def handle_start_error(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state is None:
        await message.reply("Схоже, бот не увімкнений!\n"
                            "Будь ласка, надішліть команду /start")


def register_start_error_handler(dispatcher: Dispatcher):
    dispatcher.register_message_handler(handle_start_error)
