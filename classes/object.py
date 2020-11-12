from __future__ import annotations
from typing import *
import datetime
import requests



class Object:
    all = []

    def __init__(self, d: dict, owner: 'Client') -> None:
        self.client = owner
        self.id = d["id"]
        self.name = d["name"]
        self.imei = d["imei"]
        self.all.append(self)

    @classmethod
    def get_by_name(self, name: str) -> Object:
        """
        Class method for finding objects by name.
        """
        for i in self.all:
            if i.name == name:
                return i
        raise Exception('Object not found.')

    def get_interval(self, time_from: Union[int, float], time_to: Union[int, float] = 0) -> List[dict]:
        """
        Method for getting data packets sent from a vehicle in a specified time interval.
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
        print(f'[{self.name}] Requisitando pacotes')
        packets = []
        for i in r.json()['items']:
            packets.append(i)

        while r.json()['continuation_token']  != None:
            params['from_datetime'] = r.json()['continuation_token']
            r = requests.get(self.client.locator.API_HOST + f'/objects/{self.id}/coordinates', params=params)
            for i in r.json()['items']:
                packets.append(i)
        print(f'\n{len(packets)} pacotes.')
        return packets
        

    def __repr__(self):
        return f'[Obj][{self.name}]'