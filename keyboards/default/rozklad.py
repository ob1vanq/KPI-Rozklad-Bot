from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from handlers.users.methods.times import time

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


keyboard2 = ReplyKeyboardMarkup(
    resize_keyboard= True,
    keyboard=[
        [
            KeyboardButton(text=f"Показати розклад на сьогодні")
        ],
        [
            KeyboardButton(text="Цей тиждень"),
            KeyboardButton(text="Наступний тиждень")
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

def construct(d: dict):
    long = len(d)
    keyboard = [[KeyboardButton(text = f"{i+1} {d.get(f'{i}').get('group')}")] for i in range(long)]
    keyboard.append([KeyboardButton(text="Назад")])

    return ReplyKeyboardMarkup(resize_keyboard=True,keyboard = keyboard, one_time_keyboard=True)