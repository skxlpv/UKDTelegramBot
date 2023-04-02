from aiogram import executor
from loader import dp
from bot.middlewares.menu_middleware import MenuMiddleware
from bot.handlers import search, show_schedule, start, menu, schedule_answer, handle_any_input

# Middlewares
dp.middleware.setup(MenuMiddleware())

# Handlers
handle_any_input.register_any_input_handlers(dp)
start.register_start_handlers(dp)
menu.register_menu_handlers(dp)
search.register_search_handlers(dp)
show_schedule.register_schedule_handlers(dp)
schedule_answer.register_schedule_answer_handlers(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    