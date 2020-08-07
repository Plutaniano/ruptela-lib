import requests
from .web_user import Web_User
from .object import Object

class Client:
    all = []

    def __init__(self, d, locator):
        self.index = len(Client.all)
        self.all.append(self)
        self.locator = locator
        
        self.company = d['company']
        self.phone = d['phone']
        self.id = d['id']
        self.address = d['address']
        self.email = d['email']
        self.objects = []

        self.web_users = self.create_web_users(locator)
        # pega a api_key do primeiro webuser
        # mudar para uma lista ou dict no futuro?
        self.api_key = self.web_users[0].api_key
        self.objects = self.create_objects()

    def __repr__(self):
        return f'[{self.id}] {self.company}'

    def create_web_users(self, locator):
        headers = {'X-Requested-With': 'XMLHttpRequest'}
        web_req = locator.session.get(locator.HOST + '/administrator/webusers/getList', headers=headers)
        web_users = []
        for user in web_req.json():
            if user['company'] == self.company:
                web_user = Web_User(user, locator, self)
                setattr(self, web_user.login, web_user)
                web_users.append(web_user)
        return web_users
    
    def create_objects(self):
        params={
            "version": "1",
            "api_key": self.web_users[0].api_key
        }
        objs_req = requests.get("http://api.fm-track.com/objects", params=params)
        objs = []
        for obj in objs_req.json():
            objs.append(Object(obj, self))
        return objs

    @classmethod
    def select_client(cls):
        for client in cls.all:
            print(f'[{client.index}] {client.company}')
        print('\n\n')
        index = int(input('Selecione o cliente que deseja atribuir as modificações: '))
        return cls.all[index]