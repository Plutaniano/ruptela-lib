import time
import csv
import os
from zipfile import ZipFile

from classes.operator import Operator
from classes.sim_card import Sim_Card


class Arqia(Operator):
    all = []
    
    def __init__(self):
        super().__init__('Arqia', 'estenio.benatti@excelbr.com.br', 'd79d4', 'http://arqia.saitro.com')
        self.set_options()
        self.login()
        self.get_simcards()
        

    def login(self) -> None:
        self.driver.get(self.host)
        self.driver.find_element_by_id('login').send_keys(self.username)
        form = self.driver.find_element_by_id('senha')
        form.send_keys(self.password)
        form.send_keys(self.driver.keys.RETURN)
        time.sleep(2)
        msg_bemvindo = self.driver.find_element_by_tag_name('h1').text
        if 'Seja bem-vindo à Plataforma de Consumo da Arqia' in msg_bemvindo:
            self.logged_in = True
        else:
            print(msg_bemvindo)
            self.logged_in = False
        
    def get_simcards(self) -> None:
        # limpa os relatórios existentes na pasta
        files = os.listdir('.')
        for file in files:
            if 'relatorio' in file:
                os.remove(file)

        # cria lista de arquivos antes de baixar relatório
        before_files = os.listdir('.')

        # baixa relatório de sim cards  atualizado
        self.driver.get(self.host + '/relatorios/')
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
                simcards.append(Arqia_Sim_Card(self, row))

        # limpa os arquivos baixados/utilizados
        files = os.listdir('.')
        for file in files:
            if 'relatorio' in file:
                os.remove(file)
        self.simcards = simcards


class Arqia_Sim_Card(Sim_Card):
    def __init__(self, operator: Operator, row: dict):
        super().__init__(operator, row['MSISDN'], row['ICCID'], row['Nome Fantasia'])
        self.name = row['Nome Fantasia']
        self.cpf = row['CPF/CNPJ']
        self.IMSI = row['IMSI']
        self.info = row['Info']
        self.activation = (row['Data Ativação'], row['Hora Ativação'])
        self.lastaccess = row['Data de Último Acesso']
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

if __name__ == '__main__':
    a = Arqia()
