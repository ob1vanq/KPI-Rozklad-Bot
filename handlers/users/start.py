from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart, Text

from keyboards.default.rozklad import keyboard
from loader import dp
from states.get_group_state import get_group_st,get_group_th

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    asnwer = f"Привіт {message.from_user.full_name}!\n\n" \
             f"Користуйся клавіатурою щоб дізнатсь розклад 👇"
    await message.answer(text=asnwer,reply_markup=keyboard)

@dp.message_handler(Text(equals=["Назад"]),
                    state=[get_group_st.group,get_group_st.chose,
                           get_group_th.group, get_group_st.option2, None,
                           get_group_th.group, get_group_th.chose])

async def back(message: types.Message, state: FSMContext):
    await message.answer("Ви повернулись у початок", reply_markup=keyboard)
    await state.finish()