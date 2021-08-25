from handlers.users.parsing.times import time

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from handlers.users.parsing.student import Student
from handlers.users.parsing.connection import connect
from keyboards.default.rozklad import keyboard2, keyboard, keyboard_back
from loader import dp
from states.get_group_state import get_group_st, get_group_th



@dp.message_handler(Text(equals=["Я студент 👨‍🎓"]), state=None)
async def get_user_group(message: types.Message):
    await message.answer("Вкажіть групу\n\n<i>Наприклад:</i> <pre>ДП-92</pre>",
                         parse_mode="HTML", reply_markup=keyboard_back)
    await get_group_st.group.set()


@dp.message_handler(state=get_group_st.group)
async def connect_to_site(message: types.Message, state: FSMContext):
    group = message.text
    connection = connect(group=group)

    await state.update_data(
        {
            "group": group
        }
    )

    if connection.connect():
        student = Student(connection.soup)
        is_valid_group = student.is_valid_data()

        if isinstance(is_valid_group, bool):
            await message.answer(text=f"Оберіть наступну дію", reply_markup=keyboard2)


        else:
            await message.answer(text=is_valid_group)
            await get_group_st.group.set()

    else:
        await message.answer(text=f"{connection.err}")

    await get_group_st.next()


@dp.message_handler(Text(equals=["Показати весь розклад","Перший тиждень","Другий тиждень"]), state=get_group_st.chose)
async def post_full_table(message: types.Message, state: FSMContext):
    data = await state.get_data()
    group = data.get("group")
    connection = connect(group)
    soup = connection.soup

    if connection.connect():
        student = Student(soup)
        if message.text == "Показати весь розклад":
            await message.answer("Розклад на весь тиждень", reply_markup=keyboard2)
            await student.get_full_table(message.from_user.id, group=group)
        elif message.text == "Перший тиждень":
            await message.answer("Розклад на перший тиждень", reply_markup=keyboard2)
            await student.get_full_table(message.from_user.id, group=group, week=1)
        elif message.text == "Другий тиждень":
            await message.answer("Розклад на другий тиждень", reply_markup=keyboard2)
            await student.get_full_table(message.from_user.id, group=group, week=2 , next = True)
    else:
        await message.answer(text=f"{connection.err}")




@dp.message_handler(Text(equals=[f"Показати розклад на сьогодні: {time.current_day()}"]), state=get_group_st.chose)
async def post_one_table(message: types.Message, state: FSMContext):
    data = await state.get_data()
    group = data.get("group")
    connection = connect(group)
    soup = connection.soup

    if connection.connect():
        student = Student(soup)
        await message.answer(f"Розклад на {time.current_day()}", reply_markup=keyboard2)

        str = f"<pre>{group}</pre>\n" + student.get_current_table() \
              + "\n@kpi_rozklad_bot"
        await message.answer(str, parse_mode="HTML")
    else:
        await message.answer(text=f"{connection.err}")

