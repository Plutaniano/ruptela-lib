import requests
from typing import *

from bs4 import BeautifulSoup

from .client import Client
from .hardware import Hardware, MetaHardware


# Locator

class Locator():
    HOST = 'https://track.ruptela.lt'
    API_HOST = 'http://api.fm-track.com'

    def __init__(self, username='ExcelProdutos', password='sLzN58LZ'):
        self.username = username
        self.password = password
        if self.login():
            print('--->\t Coletando informações, por favor aguarde...')
            self.get_clients(sync=True)
            MetaHardware.init(self)
            self.hardwares = Hardware.all


    def login(self) -> bool:
        self.session = requests.Session()
        params = {
            'page': 'authentication',
            'action': 'login',
            }
        data = {
            'sl': self.username,
            'ps': self.password
            }

        login_req = self.session.post(self.HOST + '/administrator/authentication/login', params=params, data=data)
        if login_req.status_code != 200:
            raise Exception('Não foi possível logar no Locator.')
        return True
    
    def get_clients(self, sync=False) -> Union[None, List[Client]]:
        headers = {
            'Connection': 'keep-alive',
            'Accept': 'application/javascript, application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-Range': 'items=0-29',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36 OPR/70.0.3728.154',
            'Range': 'items=0-29',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://track.ruptela.lt/administrator/clients',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        }
        clients_req = self.session.get(self.HOST + '/administrator/clients/getList', headers=headers)
        clients = []
        for client in clients_req.json():
            client = Client(client, self)
            clients.append(client)
        print(f'--->\t {len(clients)} clientes criados.')
        if sync:
            self.clients = clients
        else:
            return clients


    def __repr__(self) -> str:
        objs = 0
        for client in self.clients:
            objs += len(client.objects)
        return f'[Locator] <clients:{len(self.clients)} objects:{objs}>'

    def __getitem__(self, key) -> Client:
        for client in self.clients:
            if client.company == key:
                return client
        raise KeyError(f'Não foi possível encontrar um client com o nome \'{key}\'')


    def _get_phone_id(self, phone) -> str:
        phone = str(phone)
        headers = {
            'Connection': 'keep-alive',
            'Accept': 'application/javascript, application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-Range': 'items=0-99999',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.173',
            'Range': 'items=0-99999',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'http://track.ruptela.lt/administrator/connection',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        }
        r = self.session.get(self.HOST + '/administrator/connection/getList', headers=headers)
        for row in r.json():
            if row['phone'] == phone:
                return row['id'].strip()
        else:
            raise Exception('Phone not found!')


    def create_sim(self, phone, client, apn):
        print('[ * ] Criando SIM card no Locator.')
        print(f'--->\t Telefone: {phone}')
        print(f'--->\t Cliente: {client.company}')
        params = {
            'service_pr': 'Excel Produtos Eletronicos',
            'service_provider': '1407',
            'clients': str(client.id),
            'provider': '30',
            'phone': str(phone),
            'numbers': '1',
            'pin': '',
            'puk': '',
            'imsi': '',
            'ip': '',
            'apn': str(apn),
            'login': '',
            'password': '',
            'create': 'Create'
        }
        
        r = self.session.post(self.HOST + '/administrator/connection/create', params)
        soup = BeautifulSoup(r.text, 'html.parser')
        try:
            string = soup('div', 'error')[0].contents[0]
            success = False
        except:
            string = 'OK!'
            success = True
        print(f'--->\t status: {string}\n')
        return success


if __name__ == '__main__':
    l = Locator()
