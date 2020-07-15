import time
import requests
import datetime as dt

KEY = 'Al-xrBlaeH-JXIj0RuPQT6FwuPFrZZGd'
HOST = 'https://api.fm-track.com'
LOCATOR_HOST = 'http://track.ruptela.lt'

class Client:
    all = []
    def __init__(self, d, locator):
        self.index = len(Client.all)
        self.all.append(self)
        
        self.company = d['company']
        self.phone = d['phone']
        self.id = d['id']
        self.address = d['address']
        self.email = d['email']
        self.objects = []

        self.web_users = self.create_web_users(locator)

    def __repr__(self):
        return f'[{self.id}] {self.company}'

    def create_web_users(self, locator):
        headers = {'X-Requested-With': 'XMLHttpRequest'}
        web_req = locator.session.get(LOCATOR_HOST + '/administrator/webusers/getList', headers=headers)
        web_users = []
        for user in web_req.json():
            if user['company'] == self.company:
                web_user = Web_User(user, locator)
                web_users.append(web_user)
        return web_users


class Web_User:
    all = []

    def __init__(self, d, locator):
        self.all.append(self)
        self.id = int(d['id_u'])
        self.company = d['company']
        self.username = d['username']
        self.count_objects = d['count_objects']
        self.type = d['type']
        self.login = d['login']
        self.phone = d['phone']
        self.email = d['email']
        self.source = d['source']
        self.link = f'{LOCATOR_HOST}/administrator/webusers/redirectAdmin?cmd=redirect_adminTT2&id={self.id}&is_tt2=1'
        self.api_key = self.get_api_key(locator)

    def get_api_key(self, locator):
        api_key_req = locator.session.get(self.link)
        token = api_key_req.history[0].headers['Location']
        token = token.split('=')[1]
        headers = {'Authorization': token}
        api_key_req = locator.session.get('https://gtfrota.fm-track.com/gateway/user-service/v20181205/users/public-api-keys/', headers=headers)
        return api_key_req.json()['items'][0]['id']

class Object:
    all = []

    def __init__(self, d):
        self.id = d["id"]
        self.name = d["name"]
        self.imei = d["imei"]
        self.all.append(self)

    def get_by_name(name):
        for i in Object.all:
            if i.name == name:
                return i
        raise Exception('Object not found.')

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


# mudar para classe herdade de datetime
def time_convert(time):
    if isinstance(time, str):
        return dt.datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.%fZ')
    else:
        return time.isoformat()[:-7] + '.000Z'


if __name__ == '__main__':
    Client.get_clients()