import time
import requests
import json
from typing import List

from classes.operator import Operator
from classes.sim_card import Sim_Card
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


class Voxter(Operator):
    def __init__(self) -> None:
        super().__init__('Voxter', 'Ricardo@excelbr.com.br', '102030', 'http://lara.voxter.com.br')
        self.login()
        self.get_simcards()

    def login(self) -> None:
        self.driver.get(self.host + '/login.html')
        id_form = self.driver.find_element_by_id('username')
        id_form.send_keys(self.username)
        pw_form = self.driver.find_element_by_id('password')
        pw_form.send_keys(self.password)
        pw_form.send_keys(Keys.RETURN)
        time.sleep(5)

    def get_simcards(self) -> None:
        url = 'https://lara.voxter.com.br:8080/simcards/datatables'

        userdata = self.driver.execute_script("return window.localStorage.getItem('voxter-userdata');")
        userdata = json.loads(userdata)

        headers = {
            'Authorization': f"{userdata['type'].capitalize()} {userdata['token']}"
        }
        data = {
            'draw': '1',
            'columns[0][data]': '0',
            'columns[0][name]': '',
            'columns[0][searchable]': 'true',
            'columns[0][orderable]': 'false',
            'columns[0][search][value]': '',
            'columns[0][search][regex]': 'false',
            'columns[1][data]': 'fullname',
            'columns[1][name]': '',
            'columns[1][searchable]': 'true',
            'columns[1][orderable]': 'true',
            'columns[1][search][value]': '',
            'columns[1][search][regex]': 'false',
            'columns[2][data]': 'phone_company',
            'columns[2][name]': '',
            'columns[2][searchable]': 'true',
            'columns[2][orderable]': 'true',
            'columns[2][search][value]': '',
            'columns[2][search][regex]': 'false',
            'columns[3][data]': 'iccid',
            'columns[3][name]': '',
            'columns[3][searchable]': 'true',
            'columns[3][orderable]': 'true',
            'columns[3][search][value]': '',
            'columns[3][search][regex]': 'false',
            'columns[4][data]': 'line',
            'columns[4][name]': '',
            'columns[4][searchable]': 'true',
            'columns[4][orderable]': 'true',
            'columns[4][search][value]': '',
            'columns[4][search][regex]': 'false',
            'columns[5][data]': 'order',
            'columns[5][name]': '',
            'columns[5][searchable]': 'true',
            'columns[5][orderable]': 'true',
            'columns[5][search][value]': '',
            'columns[5][search][regex]': 'false',
            'columns[6][data]': 'active_date',
            'columns[6][name]': '',
            'columns[6][searchable]': 'true',
            'columns[6][orderable]': 'true',
            'columns[6][search][value]': '',
            'columns[6][search][regex]': 'false',
            'columns[7][data]': 'cancel_date',
            'columns[7][name]': '',
            'columns[7][searchable]': 'true',
            'columns[7][orderable]': 'true',
            'columns[7][search][value]': '',
            'columns[7][search][regex]': 'false',
            'columns[8][data]': 'disabled',
            'columns[8][name]': '',
            'columns[8][searchable]': 'true',
            'columns[8][orderable]': 'true',
            'columns[8][search][value]': '',
            'columns[8][search][regex]': 'false',
            'columns[9][data]': 'amount',
            'columns[9][name]': '',
            'columns[9][searchable]': 'true',
            'columns[9][orderable]': 'true',
            'columns[9][search][value]': '',
            'columns[9][search][regex]': 'false',
            'columns[10][data]': 'id',
            'columns[10][name]': '',
            'columns[10][searchable]': 'true',
            'columns[10][orderable]': 'false',
            'columns[10][search][value]': '',
            'columns[10][search][regex]': 'false',
            'order[0][column]': '1',
            'order[0][dir]': 'asc',
            'start': '0',
            'length': '999999',
            'search': '',
            'mode': '1',
            'client': '',
            'date1': '',
            'date2': ''
        }

        r = requests.post(url , headers=headers, data=data)

        sim_cards = []
        for data in r.json()['data']:
            sim = Voxter_Sim_Card(self, data)
            sim_cards.append(sim)
        
        self.simcards = sim_cards
            
        
class Voxter_Sim_Card(Sim_Card):
    def __init__(self, operator, data):
        if data['line'] == '9999999999999':
            data['line'] = None
            
        super().__init__(operator, data['line'], data['iccid'], data['fantasyname'])
        del data['line'], data['iccid'], data['fantasyname']
        for key in data.keys():
            setattr(self, key, data[key])


if __name__ == '__main__':
    v = Voxter()

