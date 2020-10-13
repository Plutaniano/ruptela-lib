from __future__ import annotations
from typing import *
import datetime
import requests



class Object:
    all = []

    def __init__(self, d, owner) -> None:
        self.client = owner
        self.id = d["id"]
        self.name = d["name"]
        self.imei = d["imei"]
        self.all.append(self)

    @classmethod
    def get_by_name(self, name) -> Object:
        """
        Class method for finding objects by name.
        """
        for i in self.all:
            if i.name == name:
                return i
        raise Exception('Object not found.')

    def get_interval(self, time_from, time_to=0) -> Union[List[dict], requests.request]:
        """
        Method for getting data from a vehicle from a specified time interval.
        """
        now = datetime.datetime.utcnow()
        time_from = (now - datetime.timedelta(days=time_from)).isoformat()[:-3] + 'Z'
        time_to = (now- datetime.timedelta(days=time_to)).isoformat()[:-3] + 'Z'
        params = {
            'version': 2,
            'api_key': self.client.web_users[0].api_key,
            'from_datetime': time_from,
            'to_datetime': time_to,
            'limit': 1000           # maximo é 1000
        }

        r = requests.get(self.client.locator.API_HOST + f'/objects/{self.id}/coordinates', params=params)
        print(f'[{self.name}] Requisitando pacotes... ', end="", flush=True)
        packets = []
        try:
            for i in r.json()['items']:
                packets.append(i)

            while r.json()['continuation_token'] != None:
                params['continuation_token'] = r.json()['continuation_token']
                r = requests.get(self.client.locator.API_HOST + f'/objects/{self.id}/coordinates', params=params)
                print('*', end='', flush=True)
                for i in r.json()['items']:
                    packets.append(i)
            print(f'\n{len(packets)} pacotes.')
            return packets

        except Exception as e:
            print('Ocorreu um erro, retornando o ultimo request para debug.')
            return r
        

    def __repr__(self):
        return f'[Obj][{self.name}]'