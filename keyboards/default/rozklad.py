from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from handlers.users.parsing.times import time

keyboard = ReplyKeyboardMarkup(
    resize_keyboard= True,
    keyboard=[
        [
            KeyboardButton(text="Я студент 👨‍🎓"),
        ],
        [
            KeyboardButton(text="Я викладач 👩‍🏫")
        ]
    ],
    one_time_keyboard = True
)

keyboard3 = ReplyKeyboardMarkup(
    resize_keyboard= True,
    keyboard=[
        [
            KeyboardButton(text=f"Показати розклад на {time.current_day()}")
        ]
    ],
    one_time_keyboard = True
)

keyboard2 = ReplyKeyboardMarkup(
    resize_keyboard= True,
    keyboard=[
        [
            KeyboardButton(text=f"Показати розклад на сьогодні: {time.current_day()}")
        ],
        [
            KeyboardButton(text="Перший тиждень"),
            KeyboardButton(text="Другий тиждень")
        ],
        [
            KeyboardButton(text="Показати весь розклад")
        ],
        [
            KeyboardButton(text="Назад"),
        ]
    ],
    one_time_keyboard = True
)

keyboard_back = ReplyKeyboardMarkup(
    resize_keyboard= True,
    keyboard=[
        [
            KeyboardButton(text="Назад"),
        ]
    ],
    one_time_keyboard = True
)