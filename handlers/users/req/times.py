import datetime
import locale

locale.setlocale(locale.LC_ALL, "uk_UA")


class time:

    __now = datetime.datetime.now()
    __next_day = __now
    __days = 0

    @staticmethod
    def update_now():
        time.__now = datetime.datetime.now()

    @staticmethod
    def date_month():
        return time.__now.strftime("%d,%B").title()


    @staticmethod
    def get_data_format(obj):
        return obj.strftime("%d,%B - %A").title()

    @staticmethod
    def next_day():
        if time.__days == 0:
            time.__next_day = time.__next_day + datetime.timedelta(days=time.__days)
            time.__days -= 1
            return time.get_data_format(time.__next_day)
        else:
            time.__days = 1
            time.__next_day = time.__next_day + datetime.timedelta(days=time.__days)
            return time.get_data_format(time.__next_day)



    @staticmethod
    def reset():
        time.__next_day = time.__now
        time.__days = 0

    @staticmethod
    def current_day():
        return time.__now.strftime("%A").title()

    @staticmethod
    def hour_minutes(text="%H:%M"):
        return time.__now.strftime(text).title()

    @staticmethod
    def day_before():
        current = time.hour_minutes("%A").lower()
        if current == 'понеділок':
            return 7
        elif current == "вівторок":
            return 6
        elif current == "середа":
            return 5
        elif current == "четвер":
            return 4
        elif current == "п'ятниця":
            return 3
        elif current == "субота":
            return 2
        elif current == "неділя":
            return 1

    @staticmethod
    def day_after():
        current = time.hour_minutes("%A").lower()
        if current == 'понеділок':
            return 0
        elif current == "вівторок":
            return 1
        elif current == "середа":
            return 2
        elif current == "четвер":
            return 3
        elif current == "п'ятниця":
            return 4
        elif current == "субота":
            return 5
        elif current == "неділя":
            return 6

    @staticmethod
    def set_week(week, current_week):
        time.__days = 0
        if week == current_week:
            time.__next_day = time.__next_day - datetime.timedelta(time.day_after())
        else:
            time.__next_day = time.__next_day + datetime.timedelta(time.day_before())

    @staticmethod
    def timeset(week, params = None):
        if week == "first":
            return {0: '08:30', 1: '10:25', 2: '12:20', 3: '14:15', 4: '16:10', 5: '18:30'}
        elif week == "second":
            timeset = dict()
            timelst = ['08:30', '10:25', '12:20', '14:15', '16:10', '18:30']
            lines = int((params.get("lines") - 2) / 2)
            indexes = [i for i in range(lines, lines*2)]
            for i in range(len(indexes)):
                timeset.update({indexes[i]:timelst[i]})
            return timeset

    @staticmethod
    def get_days_lst(params):
        column = params.get('column') - 1
        return [i for i in range(column)]


    @staticmethod
    def day_index():
        indexes = {
            "Понеділок": 0,
            "Вівторок": 1,
            "Середа": 2,
            "Четвер": 3,
            "П'ятниця": 4,
            "Субота": 5
        }
        return indexes.get(time.current_day())

    @staticmethod
    def pair_index():
        for m in range(160):
            diapazon = {0: '08:30', 1: '10:25', 2: '12:20', 3: '14:15', 4: '16:10', 5: '18:30'}
            cur = datetime.datetime.now() + datetime.timedelta(minutes=m)
            for i in range(6):
                if cur.strftime("%H:%M") == diapazon.get(i):
                    return int(i)
