from handlers.users.parsing.times import time

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from handlers.users.parsing.teacher import Teacher
from handlers.users.parsing.connection import connect
from keyboards.default.rozklad import keyboard
from loader import dp
from states.get_group_state import get_group_th


@dp.message_handler(Text(equals=["Я викладач 👩‍🏫"]), state=None)
async def get_user_group(message: types.Message):
    await message.answer("Вкажіть ПІБ\n\n<i>Наприклад:</i> <pre>Казміренко Віктор Анатолійович</pre>", parse_mode="HTML")
    await get_group_th.group.set()


@dp.message_handler(state=get_group_th.group)
async def connect_to_site(message: types.Message, state: FSMContext):
    name = message.text
    connection = connect(name=name)

    await state.update_data(
        {
            "name": name
        }
    )
    if connection.connect():
        teacher = Teacher(connection.soup)
        is_valid_name = teacher.is_valid_data()

        if isinstance(is_valid_name, bool):

            await message.answer(f"Розклад на сьогодні: {time.current_day()}", reply_markup=keyboard)
            str = f"<pre>{name}</pre>\n" + teacher.get_current_table() + \
                  "\n@kpi_rozklad_bot"
            await message.answer(str, parse_mode="HTML")
        else:
            await message.answer(is_valid_name)
    else:
        await message.answer(text=f"{connection.err}")

    await state.finish()


