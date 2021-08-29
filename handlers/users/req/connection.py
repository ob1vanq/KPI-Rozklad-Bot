import requests
import lxml
import fake_useragent

from bs4 import BeautifulSoup
from requests import ConnectionError, HTTPError


class connect:
    url_student = "http://rozklad.kpi.ua/Schedules/ScheduleGroupSelection.aspx"
    url_teacher = "http://rozklad.kpi.ua/Schedules/LecturerSelection.aspx"

    data_student = {
        "ctl00_ToolkitScriptManager_HiddenField": ";;AjaxControlToolkit,+Version=3.5.60623.0,+Culture=neutral,+PublicKeyToken=28f01b0e84b6d53e::834c499a-b613-438c-a778-d32ab4976134:22eca927:ce87be9:2d27a0fe:23389d96:77aedcab:1bd6c8d4:7b704157",

        "ctl00$MainContent$ctl00$btnShowSchedule": "Розклад занять",
        "__VIEWSTATE": "/wEMDAwQAgAADgEMBQAMEAIAAA4BDAUDDBACAAAOAgwFBwwQAgwPAgEIQ3NzQ2xhc3MBD2J0biBidG4tcHJpbWFyeQEEXyFTQgUCAAAADAUNDBACAAAOAQwFAQwQAgAADgEMBQ0MEAIMDwEBBFRleHQBG9Cg0L7Qt9C60LvQsNC0INC30LDQvdGP0YLRjAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALVdjzppTCyUtNVSyV7xykGQzHz2",
        "__EVENTTARGET": "",
        "__EVENTARGUMENT": "",
        "__EVENTVALIDATION": "/wEdAAEAAAD/////AQAAAAAAAAAPAQAAAAUAAAAIsA3rWl3AM+6E94I5Tu9cRJoVjv0LAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHfLZVQO6kVoZVPGurJN4JJIAuaU",
        "hiddenInputToUpdateATBuffer_CommonToolkitScripts": "1"
    }

    data_teacher = {
        "ctl00_ToolkitScriptManager_HiddenField": ";;AjaxControlToolkit,+Version=3.5.60623.0,+Culture=neutral,+PublicKeyToken=28f01b0e84b6d53e::834c499a-b613-438c-a778-d32ab4976134:22eca927:ce87be9:2d27a0fe:23389d96:77aedcab:1bd6c8d4:7b704157",
        "__VIEWSTATE": "/wEMDAwQAgAADgEMBQAMEAIAAA4BDAUDDBACAAAOAgwFCwwQAgwPAgEIQ3NzQ2xhc3MBD2J0biBidG4tcHJpbWFyeQEEXyFTQgUCAAAADAUNDBACAAAOAQwFAwwQAgwADwEBB29uZm9jdXMBHXRoaXMudmFsdWU9Jyc7dGhpcy5vbmZvY3VzPScnAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJkWCFbMSgxOXJsGpLI9ZU2imYY",
        "__EVENTTARGET": "",
        "__EVENTARGUMENT": "",

        "ctl00$MainContent$btnSchedule": "Розклад+занять",
        "__EVENTVALIDATION": "/wEdAAEAAAD/////AQAAAAAAAAAPAQAAAAUAAAAIsA3rWl3AM+6E94I53LbWK4YqVqwLAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACvHV09VRintN+nMH+p4yerPBpN+",
        "hiddenInputToUpdateATBuffer_CommonToolkitScripts": "1"
    }

    student = "ctl00$MainContent$ctl00$txtboxGroup"
    teacher = "ctl00$MainContent$txtboxLecturer"

    headers = {'user-agent': fake_useragent.UserAgent().random}

    def __init__(self, title: str, person: str):
        self.title = title
        if person == "student":
            self.data = connect.format_data(self, connect.data_student, p=connect.student)
            self.url = connect.url_student
        elif person == "teacher":
            self.data = connect.format_data(self, connect.data_teacher, p=connect.teacher)
            self.url = connect.url_teacher

        self.error: str
        connect.connect(self)

    def format_data(self, data, p):
        data.update({p: self.title})
        return data

    def connect(self):

        try:
            response = requests.post(self.url, headers=connect.headers, data=self.data)
            response.raise_for_status()
        except ConnectionError as err:
            self.error = f"Помилка: {err}"
            return False

        except HTTPError as err:
            self.error = f"Помилка: {err}"
            return False
        except:
            self.error = f"Відбулась невідома помилка"
        else:
            connect.soup(self, response)
            return True

    def soup(self, response):
        self.soup = BeautifulSoup(response.text, 'lxml')

    @staticmethod
    def get_soup(url):
        response = requests.get(url)
        return BeautifulSoup(response.text, 'lxml')
