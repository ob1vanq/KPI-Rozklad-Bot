from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from handlers.users.parsing.student import Student
from handlers.users.parsing.connection import connect
from loader import dp
from  states.get_group_state import get_group


@dp.message_handler(Text(equals=["Я студент 👨‍🎓", "Я викладач 👩‍🏫"]), state=None)
async def get_user_group(message: types.Message):
    if message.text == "Я студент 👨‍🎓":
        await message.answer("Вкажіть групу\n\n"
                             "<i>Наприклад: ДП-92</i>", parse_mode = "HTML")
        await get_group.group.set()
    else:
        await message.answer("Функція в розробці")


@dp.message_handler(state=get_group.group)
async def connect_to_site(message: types.Message, state: FSMContext):
    group = message.text
    connection = connect(group)
    print(connection, connection.connect())

    if connection.connect():
        await message.answer(f"Друкую розклад для {group}")
        student = Student(connection.soup)
        answer = student.get_full_table()
        await message.answer(answer, parse_mode="HTML")
        await state.finish()
    else:
        await message.answer(text=f"{connection.err}")


#
# @dp.message_handler(state=get_group.print_table)
# async def post_user_table(message: types.Message, state: FSMContext):
#     print("here")
#     data = await state.get_data()
#     soup = data.get("connect")
#
#     student = Student(soup)
#     answer = student.get_full_table()
#
#     await message.answer(answer, parse_mode = "HTML")
#     await state.finish()





