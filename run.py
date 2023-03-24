from aiogram import executor
from loader import dp
from bot.handlers import search
from bot.handlers import test_handlers

search.register_search_handlers(dp)
test_handlers.register_search_handlers(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
