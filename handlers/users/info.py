from aiogram import types
from aiogram.dispatcher.filters import Command
from loader import dp


@dp.message_handler(Command("info"))
async def info(message: types.Message):
    url = "http://rozklad.kpi.ua/Schedules/ScheduleGroupSelection.aspx"
    url_git = "https://github.com/ob1vanq"
    info = f"Бот зроблений <i>by  @engineer_spok</i>, " \
           f"та працює на основі інтернет порталу <a href = '{url}'>Розклад КПІ</a>.\n\n" \
           f"github <a href = '{url_git}'> ob1vanq</a>"

    await message.answer(info, parse_mode="HTML", disable_web_page_preview=True)