from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart, Text, Command

from keyboards.default.rozklad import keyboard
from loader import dp
from states.get_group_state import get_group_st, get_group_th

states = [get_group_st.group, get_group_st.chose,
          get_group_th.group, get_group_st.option2,
          get_group_st.option, None,
          get_group_th.group, get_group_th.chose]


@dp.message_handler(CommandStart(), state=states)
async def bot_start(message: types.Message, state: FSMContext):
    asnwer = f"Привіт {message.from_user.full_name}!\n\n" \
             f"Користуйся клавіатурою щоб дізнатсь розклад 👇"
    await message.answer(text=asnwer, reply_markup=keyboard)
    await state.finish()

@dp.message_handler(Text(equals=["Назад"]), state=states)
async def back(message: types.Message, state: FSMContext):
    await message.answer("Ви повернулись у початок", reply_markup=keyboard)
    await state.finish()

@dp.message_handler(Command("info"), state=states)
async def info(message: types.Message):
    url = "http://rozklad.kpi.ua/Schedules/ScheduleGroupSelection.aspx"
    info = f"<i>Бот працює на основі інтернет порталу <a href = '{url}'>Розклад КПІ</a>.</i>\n\n"
    await message.answer(info, parse_mode="HTML", disable_web_page_preview=True)