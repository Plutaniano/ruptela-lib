import requests
from .web_user import Web_User
from .object import Object

class Client:
    all = []

    def __init__(self, d: dict, locator):
        self.index = len(Client.all)
        self.all.append(self)
        self.locator = locator
        
        self.company = d['company']
        self.phone = d['phone']
        self.id = d['id']
        self.address = d['address']
        self.email = d['email']
        self.objects = []

        self.create_web_users()
        self.create_objects()

    def __repr__(self):
        return f'[Client] <company:{self.company}>'

    def create_web_users(self):
        headers = {'X-Requested-With': 'XMLHttpRequest'}
        web_req = self.locator.session.get(self.locator.HOST + '/administrator/webusers/getList', headers=headers)
        web_users = []
        for user in web_req.json():
            if user['company'] == self.company:
                web_user = Web_User(user, self.locator, self)
                setattr(self, web_user.login, web_user)
                web_users.append(web_user)
        self.web_users = web_users
    
    def create_objects(self):
        params={
            "version": "1",
            "api_key": self.api_key
        }
        objs_req = requests.get("http://api.fm-track.com/objects", params=params)
        objs = []
        for obj in objs_req.json():
            objs.append(Object(obj, self))
        self.objects = objs

    def find_by_name(self, name):
        for i in self.objects:
            if i.name == name:
                return i
        raise NameError('Não foi possível encontrar objeto com o nome especificado.')

    @property
    def api_key(self):
        for web_user in self.web_users:
            try:
                return web_user.api_key
            except:
                pass
        raise Exception('Não foi possível encontrar uma api key devido a falta de web users ou falta de api nos web users.')        

    @classmethod
    def select_client(cls):
        for client in cls.all:
            print(f'[{client.index}] {client.company}')
        print('\n\n')
        index = int(input('Selecione o cliente que deseja atribuir as modificações: '))
        return cls.all[index]