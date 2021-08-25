import datetime
import locale

locale.setlocale(locale.LC_ALL, "UKR")


class time:
    now = datetime.datetime.now()
    __next_day = now

    @staticmethod
    def current():
        return time.now.strftime("%d,%B").title()

    @staticmethod
    def get_data_format(obj):
        return obj.strftime("%d,%B").title()

    @staticmethod
    def next_day():
        time.__next_day = time.__next_day + datetime.timedelta(days=1)
        return time.get_data_format(time.__next_day)

    @staticmethod
    def reset():
        time.__next_day = time.now

    @staticmethod
    def current_day():
        return time.now.strftime("%A").title()

    @staticmethod
    def current_time(text = "%H:%M"):
        return time.now.strftime(text).title()

    @staticmethod
    def day_before():
        current = time.current_time("%A").lower()
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
    def set_week(week = None):
        if time.__next_day == time.now:
            time.__next_day = time.__next_day + datetime.timedelta(time.day_before())
        if week:
            time.__next_day = time.__next_day + datetime.timedelta(days=1)
