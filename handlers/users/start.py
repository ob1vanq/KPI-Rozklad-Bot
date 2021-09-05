from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart, Text, Command

from data.config import ADMINS
from keyboards.default.rozklad import keyboard
from loader import dp, bot
from states.get_group_state import student_state, teacher_state

states = [student_state.group, student_state.chose,
          teacher_state.group, student_state.option2,
          student_state.option, None,
          teacher_state.group, teacher_state.chose]


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


@dp.message_handler(Command("admin"), state=states)
async def adm(message: types.Message):
    for admin in ADMINS:
        await bot.send_message(text=f"{datetime.now()}", chat_id=admin)
