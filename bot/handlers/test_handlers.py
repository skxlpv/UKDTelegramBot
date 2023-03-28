from aiogram import types

from bot.database.pref_requests import get_preferences, toggle_pref
from loader import dp
from bot.database.schedule_requests import set_favorites, set_primary, delete_favorite, get_from_collection


# @dp.message_handler(regexp='Обране')
# async def test_database_get_favorites(message: types.Message):
#     a = get_from_collection(message.from_user.id, 'favorites')
#     await message.answer(a)


# @dp.message_handler(regexp='Обране')
# async def test_get_preferences(message: types.Message):
#     a = get_preferences(user=message.from_user.id)
#     await message.answer(a)


# @dp.message_handler(regexp='Обране')
# async def test_toggle_additional_courses(message: types.Message):
#     a = toggle_pref(message.from_user.id, 'additional_courses')
#     await message.answer(a)


# @dp.message_handler(commands=['start'])
# async def test_start_init_pref(message: types.Message):
#     initialize_user_pref(message.from_user.id)
#     await message.answer('Started')


# @dp.message_handler(commands=['test'])
# async def test_database_set_favorites(message: types.Message):
#     a = set_favorites(message.from_user.id, message.text, isTeacher=True)
#     await message.answer('a')


@dp.message_handler(commands=['test'])
async def test_database_set_primary(message: types.Message):
    a = set_primary(message.from_user.id, 701, True)
    await message.answer(a)


# @dp.message_handler()
# async def test_database_delete_favorite(message: types.Message):
#     a = delete_favorite(message.from_user.id, message.text)
#     await message.answer(a)


def register_search_handlers(dispatcher: dp):
    # dispatcher.register_message_handler(test_database_set_favorites)
    # dispatcher.register_message_handler(test_database_get_favorites)
    # dispatcher.register_message_handler(test_get_preferences)
    # dispatcher.register_message_handler(test_toggle_additional_courses)
    dispatcher.register_callback_query_handler(test_database_set_primary)
    # dispatcher.register_callback_query_handler(test_database_delete_favorite)
