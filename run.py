from aiogram import executor

from loader import dp
from bot.middlewares import cancel
from bot.handlers import search, show_schedule, start, menu, handle_any_input

cancel_middleware = cancel.CancelMiddleware()
dp.middleware.setup(cancel_middleware)

handle_any_input.register_any_input_handlers(dp)
start.register_start_handlers(dp)
menu.register_menu_handlers(dp)
search.register_search_handlers(dp)
show_schedule.register_schedule_handlers(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    