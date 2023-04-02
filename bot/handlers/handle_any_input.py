from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from loader import dp


@dp.message_handler(state='*')
async def any_input(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state is None:
        await message.reply("Схоже, бот не увімкнений!\n"
                            "Будь ласка, надішліть команду /start")


def register_any_input_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(any_input)
