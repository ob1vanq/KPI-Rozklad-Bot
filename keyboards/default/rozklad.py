from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

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