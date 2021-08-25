from bs4.element import NavigableString

from handlers.users.parsing import indexes
from handlers.users.parsing.times import time
from handlers.users.parsing.indexes import ROOM_TUPLE


def get_current_pair(obj, need_group: bool = False):
    if obj:
        string = str()
        group = ""
        string += f"🟢 <b>Поточна пара {time.current_time()}</b>" + "\n\n"
        for i in range(0, len(obj) + 1):
            cell = obj[i].find_all('a', class_='plainLink')
            for i in obj[i]:
                if isinstance(i, NavigableString) and need_group and i:
                    group += f"{i}".replace(',','')
            for i in cell:
                if i.text.startswith(ROOM_TUPLE):
                    link = i.get('href')
                    string += f"<a href ='{link}'>{i.text}</a>" + "\n"
                else:
                    string += f"{i.text}" + "\n"

            string += group
            return string
    else:
        return False


def get_pair(obj,need_group: bool = False):
    if obj:
        table = list()
        for i in range(0, len(obj)):
            string = str()
            cell = obj[i]
            if cell.find_all('a', class_="plainLink"):
                for j in cell.find_all('a', class_="plainLink"):
                    if j.text.startswith(ROOM_TUPLE):
                        link = j.get('href')
                        string += f"<a href ='{link}'>{j.text}</a>" + "\n"
                    else:
                        string += f"{j.text}\n"

                for j in obj[i]:
                    if isinstance(j, NavigableString) and j and need_group:
                        string += f"{j}".replace(',',' ')
                if need_group:
                    string+="\n"
                table.append(string)
        return table
    else:
        return 'None'

def customize_string(pair, need_group: bool = False, need_time: bool = True, need_day: bool = True):
    day_table = str()
    table = dict(enumerate(get_pair(pair, need_group)))
    time_count = 1

    if need_day:
        day_table += f"🗓<b>{time.current()}</b>" + "\n\n"

    for i in range(0, len(table)):
        if table.get(i) == 'None':
            time_count += 1
        else:
            if need_time:
                day_table += f"<i>{time_count} - {indexes.TIME_INDEXES.get(time_count)}</i>\n{table.get(i)}\n"
            else:
                day_table += f"\n{table.get(i)}\n"
            time_count += 1
    if len(day_table) < 50:
        day_table += "Пар немає 🤟"

    return day_table