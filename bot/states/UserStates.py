from aiogram.dispatcher.filters.state import State, StatesGroup


class UserStates(StatesGroup):
    manual_search = State()
    search = State()
    search_options = State()
    menu = State()
    menu_handler = State()
    get_specialty = State()
    get_year = State()
    get_group = State()
    