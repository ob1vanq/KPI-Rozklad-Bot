from aiogram.dispatcher.filters.state import StatesGroup, State


class get_group(StatesGroup):
    group = State()
    print_table = State()