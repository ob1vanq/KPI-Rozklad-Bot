import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from handlers.users.req.connection import connect
from handlers.users.req.table import Table
from handlers.users.req.times import time
from keyboards.default.rozklad import keyboard2, keyboard_back, construct
from loader import dp
from states.get_group_state import get_group_st


@dp.message_handler(Text(equals=["Я студент 👨‍🎓"]), state=None)
async def get_user_group(message: types.Message):
    await message.answer("Вкажіть групу\n\n<i>Наприклад:</i> <pre>ДП-92</pre>",
                         parse_mode="HTML", reply_markup=keyboard_back)
    await get_group_st.group.set()


@dp.message_handler(state=get_group_st.group)
async def connect_to_site(message: types.Message, state: FSMContext):
    group = message.text
    connection = connect(title=group, person="student")
    soup = connection.soup

    if connection.connect():

        if Table.chek_valid_webpage(soup):
            d = Table.chek_valid_webpage(soup)
            keyboard = construct(d)
            await message.answer(f"Оберіть групу", reply_markup=keyboard)
            await state.update_data(
                {
                    "d": d
                }
            )
            await get_group_st.option.set()

        elif isinstance(Table.is_valid_data(soup), str):
            await message.answer(text="Групи з такою назвою не знайдено!")
        else:
            await message.answer(text=f"Оберіть наступну дію", reply_markup=keyboard2)
            await state.update_data(
                {
                    "group": group
                }
            )
            await get_group_st.next()
    else:
        await message.answer(text=f"{connection.error}")


@dp.message_handler(state=get_group_st.option)
async def chose(message: types.Message, state: FSMContext):
    data = await state.get_data()
    index = int([i for i in message.text][0]) - 1
    url = "http://rozklad.kpi.ua/Schedules/" + data.get("d").get(f"{index}").get("link")
    await state.update_data(
        {
            "url": url,
            "group": message.text
        }
    )
    await message.answer(text=f"Оберіть наступну дію", reply_markup=keyboard2)
    await get_group_st.option2.set()


@dp.message_handler(Text(equals=["Цей тиждень", "Наступний тиждень"]),
                    state=[get_group_st.chose, get_group_st.option2])
async def post_full_table(message: types.Message, state: FSMContext):
    data = await state.get_data()
    group = data.get("group")
    connection = connect(title=group, person="student")

    if get_group_st.option2:
        url = data.get("url")
        soup = connect.get_soup(url)
    else:
        soup = connection.soup

    if connection.connect():
        student = Table(soup)
        if message.text == "Цей тиждень":
            await message.answer("Розклад на цей тиждень", reply_markup=keyboard2)
            week = "first" if student.current_week == "first" else "second"
            await student.get_week(chat_id=message.from_user.id, week=week)
        elif message.text == "Наступний тиждень":
            week = "second" if student.current_week == "first" else "first"
            await message.answer("Розклад на наступний тиждень", reply_markup=keyboard2)
            await student.get_week(chat_id=message.from_user.id, week=week)
    else:
        await message.answer(text=f"{connection.error}")


@dp.message_handler(Text(equals=[f"Показати розклад на сьогодні: {time.current_day()}"]),
                    state=[get_group_st.chose, get_group_st.option2])
async def post_one_table(message: types.Message, state: FSMContext):
    data = await state.get_data()
    group = data.get("group")
    connection = connect(title=group, person="student")

    if state == get_group_st.option2:
        url = data.get("url")
        soup = connect.get_soup(url)
    else:
        soup = connection.soup

    if connection.connect():
        student = Table(soup)
        await message.answer(f"Розклад на {time.current_day()}", reply_markup=keyboard2)

        str = f"<pre>{group}</pre>\n" + student.get_today()
        await message.answer(str, parse_mode="HTML", disable_web_page_preview=True)
    else:
        await message.answer(text=f"{connection.error}")
