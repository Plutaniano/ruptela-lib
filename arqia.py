from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import requests
from bs4 import BeautifulSoup
from zipfile import ZipFile
import os
import atexit


ARQIA_HOST = 'http://arqia.saitro.com'
ARQIA_LOGIN = 'estenio.benatti@excelbr.com.br'
ARQIA_PASS = 'd79d4'
ARQIA_iS = 'ODMyNQ=='

class Arqia:
    all = []
    
    def __init__(self):
        self.all.append(self)
        self.set_options()
        self.login()
        self.get_simcards()

    def login(self):
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.get(ARQIA_HOST)
        self.driver.find_element_by_id('login').send_keys(ARQIA_LOGIN)
        form = self.driver.find_element_by_id('senha')
        form.send_keys(ARQIA_PASS)
        form.send_keys(Keys.RETURN)
        time.sleep(2)
        print(self.driver.find_element_by_tag_name('h1').text)
        
    
    def get_simcards(self):
        self.driver.get(ARQIA_HOST + '/relatorios/')
        button = self.driver.find_element_by_css_selector('table tbody tr td div input')
        files = os.listdir('.')
        for file in files:
            if 'relatorio' in file:
                os.remove(file)
        files = os.listdir('.')


        button.click()
        time.sleep(1)

        for file in os.listdir('.'):
            if file not in files:
                break
        
        filename = file
        with ZipFile(filename) as f:
            f.extractall()
        with open(filename[:-4] + '.csv', 'r') as csv:
            simcards = []
            for line in csv.readlines()[1:]:
                simcards.append(Sim_Card(line))
        self.simcards = simcards

    def set_options(self):
        options = Options()
        options.headless = True
        prefs = {"download.default_directory" : f"{os.getcwd()}"}
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option("prefs",prefs)
        self.options = options

    def find_by_ICCID(self, ICCID):
        for sim in self.simcards:
            if sim.ICCID == ICCID:
                return sim
        raise Exception('ICCID não corresponde à um numero.')

    def __repr__(self):
        return f'[Arqia] {len(self.simcards)} sim cards.'

class Sim_Card:
    def __init__(self, line):
        line = line.split(';')
        self.name = line[0]
        self.cpf = line[1]
        self.ICCID = line[2]
        self.phone = line[3]
        self.IMSI = line[4]
        self.info = line[5]
        self.activation = (line[6], line[7])
        self.lastaccess = line[8]
        self.operator = line[9]
        self.plan = line[10]
        if line[11] == 'Ativo':
            self.status = True
            self.reason = ''
        else:
            self.status = False
            self.reason = line[14]
        
        if line[12] == 'Online':
            self.is_online = True
        else:
            self.is_online = False
    
    def __repr__(self):
        intl_code = self.phone[:2]
        area_code = self.phone[2:4]
        phone = self.phone[4:]
        return f'[SIM] +{intl_code} ({area_code}) {phone[:5]}-{phone[5:]}'


def exit_handler():
    for i in Arqia.all:
        i.driver.quit()
atexit.register(exit_handler)



if __name__ == '__main__':
    a = Arqia()
