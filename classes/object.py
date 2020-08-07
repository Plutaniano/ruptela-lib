class Object:
    all = []

    def __init__(self, d, owner):
        self.client = owner
        self.id = d["id"]
        self.name = d["name"]
        self.imei = d["imei"]
        self.all.append(self)

    def get_by_name(self, name):
        for i in self.all:
            if i.name == name:
                return i
        raise Exception('Object not found.')

    def get_interval(self, time_from, time_to=0):
        time_from = (dt.datetime.utcnow() - dt.timedelta(days=time_from)).isoformat()[:-3] + 'Z'
        time_to = (dt.datetime.utcnow() - dt.timedelta(days=time_to)).isoformat()[:-3] + 'Z'
        params = {
            'version': 2,
            'api_key': self.client.web_users[0].api_key,
            'from_datetime': time_from,
            'to_datetime': time_to,
            'limit': 1000           # maximo é 1000
        }

        r = requests.get(Locator.API_HOST + f'/objects/{self.id}/coordinates', params=params)
        print(f'[{self.name}] Requisitando pacotes... ', end="")
        packets = []
        try:
            for i in r.json()['items']:
                packets.append(Packet(i, self))

            while r.json()['continuation_token'] != None:
                params['continuation_token'] = r.json()['continuation_token']
                r = requests.get(Locator.HOST + f'/objects/{self.id}/coordinates', params=params)
                print('*', end='')
                sys.stdout.flush()
                for i in r.json()['items']:
                    packets.append(Packet(i, self))
        except:
            print(r.json())
        print(f'\n{len(packets)} pacotes.')
        return packets

    def __repr__(self):
        return f'[Obj][{self.name}]'