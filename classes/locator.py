from bs4 import BeautifulSoup
import requests
from typing import *

from .client import Client
from .sim_card import Sim_Card

import logging
logger = logging.getLogger(__name__)

class Locator():
    HOST = 'https://track.ruptela.lt'
    API_HOST = 'http://api.fm-track.com'
    
    def __init__(self, username: str, password: str, fast: bool = False) -> None:
        self.username = username
        self.password = password
        self.is_fast = fast

        if self.login():
            logger.info('--->\t Coletando informações, por favor aguarde...')
            self.get_clients(sync=True)
            self._set_connection_id()


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
    
    def get_clients(self, sync: bool = False) -> Union[None, List[Client]]:
        headers = {
            'Connection': 'keep-alive',
            'Accept': 'application/javascript, application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-Range': 'items=0-9999',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36 OPR/70.0.3728.154',
            'Range': 'items=0-9999',
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
        logger.info(f'{len(clients)} clientes criados.')
        if sync:
            self.clients = clients
        else:
            return clients


    def __repr__(self) -> str:
        objs = 0
        for client in self.clients:
            objs += len(client.objects)
        return f'[Locator] <clients:{len(self.clients)} objects:{objs}>'

    def __getitem__(self, key: str) -> Client:
        for client in self.clients:
            if client.company == key:
                return client
        raise KeyError(f'Não foi possível encontrar um client com o nome \'{key}\'')


    def _get_phone_id(self, sim_card: Union[str, Sim_Card]) -> str:
        if isinstance(sim_card, Sim_Card):
            line = sim_card.line
        else:
            line = sim_card

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
            if row['phone'] == line:
                return row['id'].strip()
        else:
            raise Exception('Phone not found!')

    def _set_connection_id(self) -> None:
        r = self.session.get(self.HOST + '/administrator/connection/create')
        s = BeautifulSoup(r.content, 'html.parser')
        self._service_provider = s.find('input', {'name': 'service_provider'})['value']
        self._service_pr = s.find('input', {'name': 'service_pr'})['value']



if __name__ == '__main__':
    l = Locator()
