import requests
import lxml
import fake_useragent

from bs4 import BeautifulSoup
from requests import HTTPError


class connect:

    URL = "http://rozklad.kpi.ua/Schedules/ScheduleGroupSelection.aspx"
    headers = {'user-agent': fake_useragent.UserAgent().random}

    def __init__(self, group):
        self.group = group
        self.data = connect.__data(self)
        self.err = 'OK'

        connect.connect(self)

    def __data(self):
        data = {
            "ctl00_ToolkitScriptManager_HiddenField": ";;AjaxControlToolkit,+Version=3.5.60623.0,+Culture=neutral,+PublicKeyToken=28f01b0e84b6d53e::834c499a-b613-438c-a778-d32ab4976134:22eca927:ce87be9:2d27a0fe:23389d96:77aedcab:1bd6c8d4:7b704157",
            "ctl00$MainContent$ctl00$txtboxGroup": f"{self.group}",
            "ctl00$MainContent$ctl00$btnShowSchedule": "Розклад+занять",
            "__VIEWSTATE": "/wEMDAwQAgAADgEMBQAMEAIAAA4BDAUDDBACAAAOAgwFBwwQAgwPAgEIQ3NzQ2xhc3MBD2J0biBidG4tcHJpbWFyeQEEXyFTQgUCAAAADAUNDBACAAAOAQwFAQwQAgAADgEMBQ0MEAIMDwEBBFRleHQBG9Cg0L7Qt9C60LvQsNC0INC30LDQvdGP0YLRjAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALVdjzppTCyUtNVSyV7xykGQzHz2",
            "__EVENTTARGET": "",
            "__EVENTARGUMENT": "",
            "__EVENTVALIDATION": "/wEdAAEAAAD/////AQAAAAAAAAAPAQAAAAUAAAAIsA3rWl3AM+6E94I5Tu9cRJoVjv0LAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHfLZVQO6kVoZVPGurJN4JJIAuaU",
            "hiddenInputToUpdateATBuffer_CommonToolkitScripts": "1"
        }
        return data

    def connect(self):

        try:
            response = requests.post(url=connect.URL, data=self.data, headers=connect.headers)
            response.raise_for_status()
        except HTTPError as err:
            self.err = f"Помилка: {err}"
            return False
        else:
            connect.__soup(self,response)
            return True

    def __soup(self, response):
        self.soup = BeautifulSoup(response.text, 'lxml')
