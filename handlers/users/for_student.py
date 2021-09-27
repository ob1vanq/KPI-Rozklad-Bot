from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove

from handlers.users.methods.connection import connect
from handlers.users.methods.table import Table
from handlers.users.methods.times import time
from keyboards.default.rozklad import keyboard2, keyboard_back, construct, keyboard
from loader import dp
from states.get_group_state import student_state


@dp.message_handler(Text(equals=["Я студент 👨‍🎓"]), state=None)
async def get_user_group(message: types.Message):
    await message.answer("Вкажіть групу\n\n<i>Наприклад:</i> <pre>ДП-92</pre>",
                         parse_mode="HTML", reply_markup=keyboard_back)
    await student_state.group.set()


@dp.message_handler(state=student_state.group)
async def connect_to_site(message: types.Message, state: FSMContext):
    await message.answer("<i>⌛ Підключення до серверу...</i>", parse_mode="HTML",reply_markup=ReplyKeyboardRemove())
    group = message.text
    connection = connect(title=group, person="student")

    if connection.connect():
        soup = connection.soup
        if Table.chek_valid_webpage(soup):
            d = Table.chek_valid_webpage(soup)
            keyb = construct(d)
            await message.answer(f"Оберіть групу", reply_markup=keyb)
            await state.update_data(
                {
                    "d": d
                }
            )
            await student_state.option.set()

        elif isinstance(Table.is_valid_student(soup), str):
            await message.answer(text=Table.is_valid_student(soup), reply_markup=keyboard_back)
        else:
            await message.answer(text=f"Оберіть наступну дію", reply_markup=keyboard2)
            await state.update_data(
                {
                    "group": group
                }
            )
            await student_state.next()
    else:
        await message.answer(text=f"{connection.error}", reply_markup=keyboard)
        await state.finish()


@dp.message_handler(state=student_state.option)
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
    await student_state.option2.set()


@dp.message_handler(Text(equals=["Цей тиждень", "Наступний тиждень"]),
                    state=[student_state.chose, student_state.option2])
async def post_full_table(message: types.Message, state: FSMContext):
    data = await state.get_data()
    group = data.get("group")
    connection = connect(title=group, person="student")

    if connection.connect():

        if await state.get_state() == "student_state:option2":
            url = data.get("url")
            soup = connect.get_soup(url)
        else:
            soup = connection.soup

        student = Table(soup)

        if message.text == "Цей тиждень":
            await message.answer("Розклад на цей тиждень", reply_markup=keyboard2)
            week = "first" if student.current_week == "first" else "second"
            await student.get_week(chat_id=message.from_user.id, week=week, group = group)
        elif message.text == "Наступний тиждень":
            week = "second" if student.current_week == "first" else "first"
            await message.answer("Розклад на наступний тиждень", reply_markup=keyboard2)
            await student.get_week(chat_id=message.from_user.id, week=week, group = group)
    else:
        await message.answer(text=f"{connection.error}", reply_markup=keyboard)
        await state.finish()


@dp.message_handler(Text(equals=[f"Показати розклад на сьогодні"]),
                    state=[student_state.chose, student_state.option2])
async def post_one_table(message: types.Message, state: FSMContext):
    data = await state.get_data()
    group = data.get("group")
    connection = connect(title=group, person="student")

    if connection.connect():
        if await state.get_state() == "student_state:option2":
            url = data.get("url")
            soup = connect.get_soup(url)
        else:
            soup = connection.soup
        student = Table(soup)
        await message.answer(f"Розклад на {time.current_day()}", reply_markup=keyboard2)

        str = f"<b>{group}</b>\n" + student.get_today()
        await message.answer(str, parse_mode="HTML", disable_web_page_preview=True)
    else:
        await message.answer(text=f"{connection.error}", reply_markup=keyboard)
        await state.finish()

