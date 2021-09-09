from bs4.element import NavigableString, Tag
from .times import time


class parser:
    rooms_tuple = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
    main_week = []

    def __init__(self, soup):
        self.body = [soup.find_all('tr')[i] for i in range(0, len(soup.find_all('tr')))]
        self.params = parser.get_table_params(self, self.body)
        self.cl_body = parser.clear_body(self, params=self.params, body=self.body)
        self.current_week = parser.current_week(self, soup)

    @staticmethod
    def chek_valid_webpage(soup):
        try:
            chose = [soup.find_all('table', border="0")[i] for i in range(0, len(soup.find_all('table', border="0")))]
        except:
            return False

        if chose:
            groups = []
            links = []

            for i in range(len(chose)):
                link = chose[i].find_all('a')
                td = chose[i].find_all('td')
                if td:
                    for j in td:
                        groups.append(j.text)

                for i in link:
                    links.append(i.get('href'))

            d = dict()
            for i in range(len(groups)):
                d.update({f"{i}": {"group": groups[i], "link": links[i]}})
            return d
        else:
            return False

    def get_table_params(self, obj):
        if obj:
            column = len(obj[0].find_all('td'))
            lines = len(obj)
            return dict(column=column, lines=lines)
        else:
            return {"column": 1, "lines": 1}

    def first_week_set(self):
        lines = int((self.params.get("lines") - 2) / 2)
        return [i for i in range(lines)]

    def second_week_set(self):
        lines = int((self.params.get("lines") - 2) / 2)
        return [i for i in range(lines, lines * 2)]

    @staticmethod
    def get_td(obj):
        return [[obj.find_all('td')[i]] for i in range(0, len(obj.find_all('td')))]

    @staticmethod
    def get_tr(obj):
        return [[obj.find_all('tr')[i]] for i in range(0, len(obj.find_all('tr')))]

    def clear_body(self, body, params):
        column = params.get("column")
        if column > 2:
            del body[int(params.get("lines") / 2)]
            del body[0]

        lines = list()

        for tr in self.body:
            line = parser.get_td(tr)
            del line[0]
            line = [parser.get_pair(self, td) for td in line]
            line = dict(enumerate(line))
            lines.append(line)

        return dict(enumerate(lines))

    def get_pair(self, obj):
        table = list()
        string = str()
        for i in range(0, len(obj)):
            cell = obj[i]
            if cell.find_all('a', class_="plainLink"):
                for j in cell.find_all('a', class_="plainLink"):
                    if j.text.startswith(parser.rooms_tuple):
                        link = j.get('href')
                        if "Прак" in j.text:
                            string += " 📒"
                        elif "Лек" in j.text:
                            string += " 📚"
                        elif "Лаб" in j.text:
                            string += " 🔬"
                        string += f"<a href ='{link}'>{j.text}</a>" + "\n"
                    else:
                        string += f"{j.text}\n"
                for j in obj[i]:
                    if isinstance(j, NavigableString):
                        string += f"{j}"
                string += "\n\n"
            else:
                return "0"
        table.append(string.replace(",", ""))
        return table

    def get_current_pair(self, obj):
        string = str()
        group = ""
        string += f"🟢 <b>Поточна пара {time.hour_minutes()}</b>" + "\n\n"
        for i in range(0, len(obj) + 1):
            cell = obj[i].find_all('a', class_="plainLink")
            for i in obj[i]:
                if isinstance(i, NavigableString):
                    group += f"{i}".replace(',', '')
            for i in cell:
                if i.text.startswith(parser.rooms_tuple):
                    link = i.get('href')
                    if "Прак" in i.text:
                        string += " 📒"
                    elif "Лек" in i.text:
                        string += " 📚"
                    elif "Лаб" in i.text:
                        string += " 🔬"
                    string += f"<a href ='{link}'>{i.text}</a>" + "\n"
                else:
                    string += f"{i.text}" + "\n"

            string += group + "\n\n"
            return [string]

    def today(self, soup):
        current_pair = [soup.find_all('td', class_="current_pair")[i] for i in
                        range(0, len(soup.find_all('td', class_="current_pair")))]
        day_backlight = [soup.find_all('td', class_="day_backlight")[i] for i in
                         range(0, len(soup.find_all('td', class_="day_backlight")))]
        closest_pair = [soup.find_all('td', class_="closest_pair")[i] for i in
                        range(0, len(soup.find_all('td', class_="closest_pair")))]

        index = 10
        long = int()
        pair = str()


        if current_pair:
            index = time.pair_index() - 1
            pair = parser.get_current_pair(self, current_pair)
            long = index + 1

        if closest_pair and time.is_now_pair(parser.how_pair_today(self)):
            for i in parser.main_week:
                pairs = i.find_all('td', class_="closest_pair")
                if pairs == closest_pair:
                    index = parser.get_closest_index(self)
                    pair = ["<b>⏩ Наступна пара\n\n</b>" + parser.get_pair(self, closest_pair)[0]]
                    long = index + 1
                else:
                    long = len(day_backlight)
        if day_backlight:
            long = len(day_backlight)

        lines = list()
        for td in range(long):
            if td == index:
                lines.append(pair)
            line = parser.get_pair(self, [day_backlight[td]])
            lines.append(line)

        return dict(enumerate(lines))

    def current_week(self, soup):

        first = [soup.find_all('table', id='ctl00_MainContent_FirstScheduleTable')[i] for i in
                range(0, len(soup.find_all('table', id='ctl00_MainContent_FirstScheduleTable')))]

        second = [soup.find_all('table', id='ctl00_MainContent_SecondScheduleTable')[i] for i in
                range(0, len(soup.find_all('table', id='ctl00_MainContent_SecondScheduleTable')))]

        if first[0].find_all("td", class_ = "day_backlight"):
            parser.main_week = first
            return "first"
        elif second[0].find_all("td", class_ = "day_backlight"):
            parser.main_week = second
            return "second"
        elif not second[0].find_all("td", class_ = "day_backlight") and second[0].find_all("td", class_ = "closest_pair"):
            parser.main_week = first
            return "first"
        elif not second[0].find_all("td", class_ = "day_backlight") and second[0].find_all("td", class_ = "closest_pair"):
            parser.main_week = second
            return "second"



    def get_closest_index(self):
        body = self.main_week[0]
        body = parser.get_tr(body)
        del body[0]
        for i in range(len(body)):
            if body[i][0].find_all('td', class_ = 'closest_pair'):
                return i

    def how_pair_today(self):
        count = 0
        day = time.day_index()
        week = parser.first_week_set(self) if self.current_week == "first" else parser.second_week_set(self)
        body = self.cl_body

        for i in week:
            if body.get(i).get(day) != '0':
                count += 1
        return count - 1
