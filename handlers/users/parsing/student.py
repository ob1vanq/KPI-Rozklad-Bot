
import indexes
from times import time
# from .times import time

class Student:

    timedata = time()

    def __init__(self, soup = None):
        if soup:
            self.__soup = soup
        self.week = 1
        self.day = 0
        self.err: str = "No truble"

    def __get_table(self, week):

        soup = self.__soup
        # Список всех объектов таблици расписания
        body = [(soup.find_all('td'))[i] for i in range(0, len((soup.find_all('td'))))]

        # Список расписания: название предмета + кабинет
        table = list()

        for count in indexes.CELL_INDEXES.get(week):
            string = str()
            # Одна ячейка из расписания
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

    def get_day_table(self, week=None, day=None):

        NOT_GROUP = self.__soup.find('span', id="ctl00_MainContent_ctl00_lblError")

        if NOT_GROUP:
            return NOT_GROUP.text

        if week:
            pass
        else:
            week = self.week
        if day:
            pass
        else:
            day = self.day

        table = dict(enumerate(Student.__get_table(self, week=week)))
        time_count = 1
        day_table = str()

        if week == 1 and day == 0:
            next_day = Student.timedata.current
        elif week == 2 and day == 0:
            Student.timedata.next_day()
            next_day = Student.timedata.next_day()
        else:
            next_day = Student.timedata.next_day()

        day_table += f"<b>{indexes.DAY_INDEXES.get(day)} {next_day}</b>" + "\n"

        for i in range(day, indexes.all_cells, 6):
            if table.get(i) == 'None':
                time_count += 1
            else:
                day_table += f"🗓<i>{time_count} - {indexes.TIME_INDEXES.get(time_count)}</i>\n{table.get(i)}\n"
                time_count += 1

        return day_table

    def get_week_table(self, week):
        week_table = str()
        for day in [0,1,2,3,4,5]:
            week_table += Student.get_day_table(self, day=day,week=week)
        return week_table

    def get_full_table(self):
        full_table = str()
        for week in [1, 2]:
            for day in [0,1,2,3,4,5]:
                full_table += Student.get_day_table(self, day=day,week=week)
        return full_table


