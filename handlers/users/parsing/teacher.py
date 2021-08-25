from . import indexes
from .times import time
from .functions import get_current_pair, get_pair, customize_string

class Teacher:

    timedata = time()

    def __init__(self, soup):
        self.__soup = soup

    def is_valid_data(self):
        not_group = self.__soup.find('span', id="ctl00_MainContent_ctl00_lblError")
        if not_group:
            return not_group.text
        else:
            return True

    def get_current_table(self):
        soup = self.__soup


        current_pair = [soup.find_all('td', class_="current_pair")[i] for i in
                        range(0, len(soup.find_all('td', class_="current_pair")))]
        closest_pair = [soup.find_all('td', class_="closest_pair")[i] for i in
                       range(0, len(soup.find_all('td', class_="closest_pair")))]
        day_backlight = [soup.find_all('td', class_="day_backlight")[i] for i in
                         range(0, len(soup.find_all('td', class_="day_backlight")))]

        if get_current_pair(current_pair):
            print("cur")
            day_table = str(customize_string(day_backlight, need_group=True))
            return f"🗓<b>{time.current()}</b>\n\n" \
                   f"{get_current_pair(current_pair, need_group= True)}\n" \
                   f"<b>Інші пари</b>\n\n" + day_table


        else:
            Teacher.timedata.reset()
            if int(time.current_time("%H")) > 18:
                string = f"<b>⏩ Наступна пара: {Teacher.timedata.next_day()}</b>\n"
            else:
                string = f"<b>⏩ Наступна пара</b>\n"

            day_table = customize_string(day_backlight) + string + \
                        customize_string(closest_pair, need_group= True, need_time= False, need_day = False)

            return day_table








