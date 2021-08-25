from typing import Optional

from . import indexes
from .times import time
from loader import bot
from .functions import get_pair, get_current_pair, customize_string


class Student:
    timedata = time()

    def __init__(self, soup):
        self.__soup = soup

    def is_valid_group(self):
        not_group = self.__soup.find('span', id="ctl00_MainContent_ctl00_lblError")
        if not_group:
            return not_group.text
        else:
            return True

    def __get_table(self, week):

        soup = self.__soup
        body = [(soup.find_all('td'))[i] for i in range(0, len((soup.find_all('td'))))]

        table = list()

        for count in indexes.CELL_INDEXES.get(week):
            string = str()
            cell = body[count].find_all('a', class_='plainLink')
            if not cell:
                string += 'None'
            else:
                for i in cell:
                    if i.text.startswith(indexes.ROOM_TUPLE):
                        link = i.get('href')
                        string += f"<a href ='{link}'>{i.text}</a>" + "\n"
                    else:
                        string += f"{i.text}" + "\n"

            table.append(string)
        return table

    def get_current_table(self):

        soup = self.__soup

        current_pair = [soup.find_all('td', class_="current_pair")[i] for i in
                        range(0, len(soup.find_all('td', class_="current_pair")))]

        closest_pair = [soup.find_all('td', class_="closest_pair")[i] for i in
                        range(0, len(soup.find_all('td', class_="closest_pair")))]

        day_backlight = [soup.find_all('td', class_="day_backlight")[i] for i in
                         range(0, len(soup.find_all('td', class_="day_backlight")))]

        if get_current_pair(current_pair):
            return f"🗓<b>{time.current()}</b>\n\n" \
                   f"{get_current_pair(current_pair)}\n" \
                   f"<b>📔 Інші пари</b>\n" + customize_string(day_backlight,need_time=False, need_day=False)

        if int(time.current_time("%H")) <= 9:
            return customize_string(day_backlight) + f"⏩<b>Наступна пара</b>\n{get_pair(closest_pair)}\n"

        if not get_current_pair(current_pair):
            return customize_string(day_backlight)

    def get_day_table(self, week, day, next = False):


        table = dict(enumerate(Student.__get_table(self, week=week)))
        time_count = 1
        day_table = str()


        # Настройки отображения даты
        if week == 1 and day == 0:
            next_day = Student.timedata.current()
        elif next:
            time.set_week()
            next_day = Student.timedata.next_day()
        elif week == 2 and day == 0:
            time.set_week(True)
            next_day = Student.timedata.next_day()
        else:
            next_day = Student.timedata.next_day()

        # Парсинг
        day_table += f"🗓<b>{indexes.DAY_INDEXES.get(day)} {next_day}</b>" + "\n\n"

        for i in range(day, indexes.all_cells, 6):
            if table.get(i) == 'None':
                time_count += 1
            else:
                day_table += f"<i>{time_count} - {indexes.TIME_INDEXES.get(time_count)}</i>\n{table.get(i)}\n"
                time_count += 1
        if len(day_table) < 50:
            day_table += "Пар немає 👌\n"
        return day_table

    async def get_full_table(self, chat_id, group, week=None, next = False):
        Student.timedata.reset()
        if week:
            lst = [week]
        else:
            lst = [1, 2]
        for w in lst:
            for day in [0, 1, 2, 3, 4, 5]:
                str = f"{group}, тиждень - {w}\n" + Student.get_day_table(self, day=day, week=week, next=next) + \
                      "\n@kpi_rozklad_bot"

                await bot.send_message(text=str, chat_id=chat_id, parse_mode="HTML")
