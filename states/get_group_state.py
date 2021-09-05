from aiogram.dispatcher.filters.state import StatesGroup, State


class student_state(StatesGroup):
    group = State()
    chose = State()
    option = State()
    option2 = State()


class teacher_state(StatesGroup):
    group = State()
    chose = State()

