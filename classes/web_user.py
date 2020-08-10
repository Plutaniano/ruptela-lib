class Web_User:
    all = []

    def __init__(self, d, locator, owner):
        self.all.append(self)
        self.locator = locator
        self.client = owner
        self.id = int(d['id_u'])
        self.company = d['company']
        self.username = d['username']
        self.count_objects = d['count_objects']
        self.type = d['type']
        self.login = d['login']
        self.phone = d['phone']
        self.email = d['email']
        self.source = d['source']
        self.link = f'{locator.HOST}/administrator/webusers/redirectAdmin?cmd=redirect_adminTT2&id={self.id}&is_tt2=1'
        try:
            self.api_key = self.get_api_key(locator)
        except:
            pass

    def get_api_key(self, locator):
        api_key_req = locator.session.get(self.link)
        token = api_key_req.history[0].headers['Location']
        token = token.split('=')[1]
        headers = {'Authorization': token}
        api_key_req = locator.session.get('https://gtfrota.fm-track.com/gateway/user-service/v20181205/users/public-api-keys/', headers=headers)
        try:
            key = api_key_req.json()['items'][0]['id']
        except:
            key = []
        return key
        
    def __repr__(self):
        return f'[web id:{self.id}] {self.username}'