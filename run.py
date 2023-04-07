from aiogram import executor
from bot.handlers import (search, start, menu, settings,
                          schedule_buttons_handler, settings_buttons_handler,
                          handle_start_error)
from bot.middlewares.cancel_middleware import CancelMiddleware
from bot.middlewares.settings_middleware import SettingsMiddleware
from bot.middlewares.start_middleware import StartMiddleware
from loader import dp

# Middlewares
dp.middleware.setup(CancelMiddleware())
dp.middleware.setup(SettingsMiddleware())
dp.middleware.setup(StartMiddleware())

# Handlers
start.register_start_handlers(dp)
settings.register_settings_handler(dp)
menu.register_menu_handlers(dp)
search.register_search_handlers(dp)
schedule_buttons_handler.register_schedule_answer_handlers(dp)
settings_buttons_handler.register_schedule_answer_handlers(dp)
handle_start_error.register_start_error_handler(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    