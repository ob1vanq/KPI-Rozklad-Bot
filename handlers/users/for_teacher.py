
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from handlers.users.req.connection import connect
from handlers.users.req.table import Table
from handlers.users.req.times import time
from keyboards.default.rozklad import keyboard2
from loader import dp
from states.get_group_state import get_group_th


@dp.message_handler(Text(equals=["Я викладач 👩‍🏫"]), state=None)
async def get_user_group(message: types.Message):
    await message.answer("Вкажіть ПІБ\n\n<i>Наприклад:</i> <pre>Казміренко Віктор Анатолійович</pre>", parse_mode="HTML")
    await get_group_th.group.set()


@dp.message_handler(state=get_group_th.group)
async def connect_to_site(message: types.Message, state: FSMContext):
    name = message.text
    connection = connect(title=name, person="teacher")
    soup = connection.soup

    await state.update_data(
        {
            "name": name
        }
    )
    if connection.connect():
        teacher = Table(connection.soup)

        if isinstance(Table.is_valid_data(soup), str):
            await message.answer(text=Table.is_valid_data(soup))
            await get_group_th.group.set()
        else:
            await message.answer(text=f"Оберіть наступну дію", reply_markup=keyboard2)
            await get_group_th.next()
    else:
        await message.answer(text=f"{connection.error}")


@dp.message_handler(Text(equals=["Цей тиждень" ,"Наступний тиждень"]), state=get_group_th.chose)
async def post_full_table(message: types.Message, state: FSMContext):
    data = await state.get_data()
    name = data.get("name")
    connection = connect(title=name, person="teacher")
    soup = connection.soup

    if connection.connect():
        teacher = Table(soup)
        if message.text == "Цей тиждень":
            await message.answer("Розклад на цей тиждень", reply_markup=keyboard2)
            week = "first" if teacher.current_week == "first" else "second"
            await teacher.get_week(chat_id = message.from_user.id, week= week)
        elif message.text == "Наступний тиждень":
            week = "second" if teacher.current_week == "first" else "first"
            await message.answer("Розклад на наступний тиждень", reply_markup=keyboard2)
            await teacher.get_week(chat_id = message.from_user.id, week = week)
    else:
        await message.answer(text=f"{connection.error}")

@dp.message_handler(Text(equals=[f"Показати розклад на сьогодні: {time.current_day()}"]), state=get_group_th.chose)
async def post_one_table(message: types.Message, state: FSMContext):
    data = await state.get_data()
    name = data.get("name")
    connection = connect(title=name, person="teacher")
    soup = connection.soup

    if connection.connect():
        teacher = Table(soup)
        await message.answer(f"Розклад на {time.current_day()}", reply_markup=keyboard2)

        str = f"<pre>{name}</pre>\n" + teacher.get_today()
        await message.answer(str, parse_mode="HTML", disable_web_page_preview=True)
    else:
        await message.answer(text=f"{connection.error}")