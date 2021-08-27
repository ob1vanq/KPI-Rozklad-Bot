from aiogram.dispatcher.filters.state import StatesGroup, State


class get_group_st(StatesGroup):
    group = State()
    chose = State()
    option = State()
    option2 = State()


class get_group_th(StatesGroup):
    group = State()
    chose = State()

