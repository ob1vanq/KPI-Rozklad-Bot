import datetime
import locale

locale.setlocale(locale.LC_ALL, "UKR")


class time:
    now = datetime.datetime.now()
    __next_day = now

    def __init__(self):
        self.current = time.now.strftime("%d,%B").title()

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
