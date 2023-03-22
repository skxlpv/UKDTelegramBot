from aiogram import executor
from loader import dp
from bot.handlers import search, show_schedule

search.register_search_handlers(dp)
show_schedule.register_schedule_handlers(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    