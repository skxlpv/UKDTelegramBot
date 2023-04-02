from aiogram.dispatcher.filters.state import State, StatesGroup


class UserStates(StatesGroup):
    # MENU STATES
    # general menu states
    start = State()
    menu = State()
    menu_handler = State()

    # SEARCH STATES
    # general search states
    search = State()
    search_options = State()
    manual_search = State()

    # student search by criteria states
    get_specialty = State()
    get_year = State()
    get_group = State()

    # teacher search states
    search_teacher = State()
    get_teacher_schedule = State()

    # schedule state
    my_schedule = State()
    schedule_callback = State()
    tip_callback = State()
