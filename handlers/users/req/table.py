from loader import bot
from .parsing import parser
from .times import time

class Table(parser):

    url = "http://rozklad.kpi.ua/Schedules/ScheduleGroupSelection.aspx"

    def __init__(self, soup):
        self.soup = soup
        super().__init__(soup)



    @staticmethod
    def is_valid_student(soup):
        not_group = soup.find('span', id="ctl00_MainContent_ctl00_lblError")
        if not_group:
            return not_group.text

    @staticmethod
    def is_valid_teacher(soup):
        not_name = soup.find('span', id="ctl00_MainContent_lblError")
        if not_name:
            return not_name.text

    async def get_week(self, week, chat_id):

        time.reset()
        timeset = time.timeset(week, params=self.params)

        body = self.cl_body
        w = list()

        time.set_week(week = week, current_week=self.current_week)

        if week == "first":
            w = Table.first_week_set(self)
        elif week == "second":
            w = Table.second_week_set(self)

        for j in time.get_days_lst(self.params):
            table = f"🗓<b>{time.next_day()}\n\n</b>"
            for i in w:
                line = body.get(i).get(j)
                line = line[0]
                # print(line)
                if line != "0":
                    table += f"<i>{timeset.get(i)}</i>\n{line}"

            if len(table)<40:
                table += "Пар немає 👌\n\n"
            table += "@kpi_rozklad_bot"
            await bot.send_message(text=table, chat_id=chat_id, parse_mode="HTML", disable_web_page_preview=True)

    def get_today(self):
        timeset = time.timeset(week = "first")
        body = Table.today(self, soup=self.soup)
        table = str()

        table += f"🗓 <b>{time.date_month()}</b>\n\n"
        for i in range(len(body)):
            line = body.get(i)
            line = line[0]

            if line != "0":
                table += f"<i>{i+1} - {timeset.get(i)}</i>\n{line}"
        if len(table) < 50:
            table += "Пар немає 👌\n"
        table += "\n@kpi_rozklad_bot"
        return table




