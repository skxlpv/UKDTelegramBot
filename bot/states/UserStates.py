from aiogram.dispatcher.filters.state import State, StatesGroup


class UserStates(StatesGroup):
    specialty = State()
    year = State()
    group = State()
    