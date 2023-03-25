from aiogram import types
from loader import dp
from bot.database.schedule_requests import set_favorites, set_primary, delete_favorite

#
# @dp.message_handler()
# async def test_database_set_favorites(message: types.Message):
#     a = set_favorites(message.from_user.id, message.text, isTeacher=True)
#     await message.answer(a)


# @dp.message_handler()
# async def test_database_set_primary(message: types.Message):
#     a = set_primary(message.from_user.id, message.text)
#     await message.answer(a)


# @dp.message_handler()
# async def test_database_delete_favorite(message: types.Message):
#     a = delete_favorite(message.from_user.id, message.text)
#     await message.answer(a)


def register_search_handlers(dispatcher: dp):
    pass
    # dispatcher.register_message_handler(test_database_set_favorites)
    # dispatcher.register_callback_query_handler(test_database_set_primary)
    # dispatcher.register_callback_query_handler(test_database_delete_favorite)
