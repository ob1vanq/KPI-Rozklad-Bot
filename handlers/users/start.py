from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default.rozklad import keyboard
from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    asnwer = f"Привіт {message.from_user.full_name}!" \
             f"Користуйся клавіатурою щоб дізнатсь розклад"
    await message.answer(text=asnwer,reply_markup=keyboard)