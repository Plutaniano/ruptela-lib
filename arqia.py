from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import csv
import requests
from bs4 import BeautifulSoup
from zipfile import ZipFile
import os
import atexit


ARQIA_HOST = 'http://arqia.saitro.com'
ARQIA_LOGIN = 'estenio.benatti@excelbr.com.br'
ARQIA_PASS = 'd79d4'

class Arqia:
    all = []
    
    def __init__(self):     # inicializa o objeto Arqia com alguns atributos
        self.all.append(self)
        self.set_options()
        self.login()
        self.get_simcards()
        

    def login(self):    # abre o browser e faz login no site da Arqia
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.get(ARQIA_HOST)
        self.driver.find_element_by_id('login').send_keys(ARQIA_LOGIN)
        form = self.driver.find_element_by_id('senha')
        form.send_keys(ARQIA_PASS)
        form.send_keys(Keys.RETURN)
        time.sleep(2)
        msg_bemvindo = self.driver.find_element_by_tag_name('h1').text
        if 'Seja bem-vindo à Plataforma de Consumo da Arqia' in msg_bemvindo:
            self.logged_in = True
        else:
            print(msg_bemvindo)
            self.logged_in = False
        
    def get_simcards(self):
        # limpa os relatórios existentes na pasta
        files = os.listdir('.')
        for file in files:
            if 'relatorio' in file:
                os.remove(file)

        # cria lista de arquivos antes de baixar relatório
        before_files = os.listdir('.')

        # baixa relatório de sim cards  atualizado
        self.driver.get(ARQIA_HOST + '/relatorios/')
        button = self.driver.find_element_by_css_selector('table tbody tr td div input')
        button.click()
        time.sleep(1)

        # compara a lista de arquivos antes de baixar o relatório com
        # a lista de arquivos após o download, sai do loop com o arquivo novo em 'file'
        file = ''
        for file in os.listdir('.'):
            if file not in before_files:
                break
        
        # extrai o .csv do .zip, lê cada linha do arquivo .csv e cria os objetos Sim_Card
        if file == '':
            raise FileNotFoundError('Não foi possível baixar o relatório de sim cards.')
        filename = file

        with ZipFile(filename) as f:
            f.extractall()
        with open(filename[:-4] + '.csv', 'r') as f:
            csv_reader = csv.DictReader(f, delimiter=';')
            simcards = []
            for row in csv_reader:
                simcards.append(Sim_Card(row))

        # limpa os arquivos baixados/utilizados
        files = os.listdir('.')
        for file in files:
            if 'relatorio' in file:
                os.remove(file)

        # salva a lista de Sim_Cards no atributo simcards
        self.simcards = simcards

    def set_options(self):      #define algumas opções para o browser "virtual"
        options = Options()
        options.headless = True
        prefs = {"download.default_directory" : f"{os.getcwd()}"}
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option("prefs",prefs)
        self.options = options

    def find_by_ICCID(self, ICCID):     # retorna o objeto Sim_Card correspondente ao ICCID inputado
        for sim in self.simcards:
            if sim.ICCID == ICCID:
                return sim
        raise KeyError('ICCID não corresponde a um numero.')

    def __repr__(self):
        return f'[Arqia] {len(self.simcards)} sim cards.'

class Sim_Card:
    def __init__(self, row):
        self.name = row['Nome Fantasia']
        self.cpf = row['CPF/CNPJ']
        self.ICCID = row['ICCID']
        self.phone = row['MSISDN']
        self.IMSI = row['IMSI']
        self.info = row['Info']
        self.activation = (row['Data Ativação'], row['Hora Ativação'])
        self.lastaccess = row['Data de Último Acesso']
        self.operator = row['Operadora']
        self.plan = row['Plano']
        self.LBS = row['LBS']
        if row['Status'] == 'Ativo':
            self.status = True
            self.reason = row['Bloqueio/Suspensão']
        else:
            self.status = False
            self.reason = row['Bloqueio/Suspensão']
        
        if row['Conexão'] == 'Online':
            self.is_online = True
        else:
            self.is_online = False
    
    def __repr__(self):
        intl_code = self.phone[:2]
        area_code = self.phone[2:4]
        phone = self.phone[4:]
        return f'[SIM] +{intl_code} ({area_code}) {phone[:5]}-{phone[5:]}'



def exit_handler():     
    # fecha os browsers abertos quando o programa é encerrado
    for i in Arqia.all:
        i.driver.quit()
atexit.register(exit_handler)


if __name__ == '__main__':
    a = Arqia()
