
from student import Student
from connection import connect
from times import time
from indexes import DAY_INDEXES

connect = connect("ДМ-92")

gr = Student(connect.soup)

if time.current_day() != "Неділя":
    print(gr.get_day_table(DAY_INDEXES.get(time.current_day())))









