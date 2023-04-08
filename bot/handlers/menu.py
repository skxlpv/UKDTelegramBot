from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from bot.database.schedule_requests import get_from_collection
from bot.handlers import search, favorites, settings
from bot.keyboards.inline.yes_or_not_keyboard import tip_keyboard
from bot.keyboards.reply.menu_keyboard import menu_keyboard
from bot.states.UserStates import UserStates
from bot.storage.placeholders import buttons, messages
from bot.utils.schedule_utils import get_teacher_or_group
from bot.utils.search_utils import clear_all_keyboards
from loader import dp


@dp.message_handler(state=UserStates.menu)
async def menu(message: types.Message):
    clear_all_keyboards()
    await message.answer(text=messages.PICK_OPTION, reply_markup=menu_keyboard)
    await UserStates.menu_handler.set()


@dp.message_handler(state=(UserStates.menu_handler, '*'))
async def menu_handler(message: types.Message, state: FSMContext):

    if message.text == '/settings':
        await settings.settings_handler()

    if message.text == buttons.FIND_SCHEDULE:
        await UserStates.search.set()
        await search.search_schedule(message=message)

    elif message.text == buttons.MY_SCHEDULE:
        primary = get_from_collection(message.from_user.id, 'primary')
        hasPrimary = await get_teacher_or_group(primary, message, state)

        if hasPrimary is False:
            await message.answer(text=messages.TIP, reply_markup=tip_keyboard)
            await UserStates.tip_callback.set()

    elif message.text == buttons.FAVORITES:
        await UserStates.show_favorites.set()
        await favorites.show_favorites(message=message, state=state)


def register_menu_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(menu)
    dispatcher.register_message_handler(menu_handler)
