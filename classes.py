import time
import requests
import datetime as dt
import matplotlib.pyplot as plt

URL = "https://api.fm-track.com/"
KEY = 'Al-xrBlaeH-JXIj0RuPQT6FwuPFrZZGd'
HOST = 'http://api.fm-track.com'


class Object:
    all = []

    def __init__(self, d):
        self.id = d["id"]
        self.name = d["name"]
        self.imei = d["imei"]
        self.all.append(self)

    def get(**kwargs):
        try:
            for key in kwargs.keys():
                for obj in Object.all:
                    if getattr(obj, key) == kwargs[key]:
                        return obj
            print('Nao foi possivel encontrar o objeto')
        except:
            raise ValueError('Nao foi possivel encontrar o objeto')

    def __repr__(self):
        return f'[Obj][{self.name}]'

    def get_interval(self, time_from, time_to=0, *args):
        time_from = (dt.datetime.utcnow() - dt.timedelta(days=time_from)).isoformat()[:-3] + 'Z'
        time_to = (dt.datetime.utcnow() - dt.timedelta(days=time_to)).isoformat()[:-3] + 'Z'
        params = {
            'version': 2,
            'api_key': KEY,
            'from_datetime': time_from,
            'to_datetime': time_to,
            'limit': 1000
        }

        r = requests.get(HOST + f'/objects/{self.id}/coordinates', params=params)
        print(r)
        try:
            for i in r.json()['items']:
                yield i

            while r.json()['continuation_token'] != None:
                params['continuation_token'] = r.json()['continuation_token']
                r = requests.get(HOST + f'/objects/{self.id}/coordinates', params=params)
                for i in r.json()['items']:
                    yield i
        except:
            print(r.json())


class Packet:
    def __init__(self, d):
        self.object_id = d['object_id']
        self.datetime = time_convert(d['datetime'])
        self.ignition_status = d['ignition_status']
        self.position = d['position']
        self.virtual_gps_odometer = d['inputs']['other']['virtual_gps_odometer']
        try:
            self.gsm_signal_strength = d['inputs']['device_inputs']['gsm_signal_strength']
        except:
            self.gsm_signal_strength = 0
        self.virtual_odometer = d['inputs']['device_inputs']['virtual_odometer']

    def __repr__(self):
        return f'[...{self.object_id[-3:]}][{self.datetime.isoformat()}] [{self.gsm_signal_strength}]'


class Client:
    all = []
    def __init__(self, d):
        self.index = len(Client.all)
        self.all.append(self)
        for key in d:
            setattr(self, key, d[key])

    def __repr__(self):
        return f'[ID:{self.index}] {self.company}'

def create_all_objects():
    params = {
        "version": "1",
        "api_key": key,
    }

    print('Criando objetos...')
    r = requests.get(URL + 'objects', params=params)
    for i in r.json():
        Object(i)


def time_convert(time):
    if isinstance(time, str):
        return dt.datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.%fZ')
    else:
        return time.isoformat()[:-7] + '.000Z'


if __name__ == '__main__':
    create_all_objects()
