from typing import *

class Web_User:
    """
    Class for storing data and methods related to a locator's web user.

    ...

    Class Attributes:

        all: list
            A list containing all Web_User instances.
    ...

    Attributes:

        locator: Locator
            The locator that 'owns' this web user.

        client: Client
            The client that 'owns' this web user.

        id: int
            The id of the web user in the locator.

        company: str
            The name of the company that owns this web users.

        username: str
            Name of the user.
        
        count_objects: int
            Not used, defaults to 0.

        is_admin: bool
            True for admin, False for user.

        login: str
            Login used to authenticate this web user into TrustTrack.

        phone: str
            Phone of the web user.
        
        email: str
            Email of the web user.

        source: str
            Place where user was created. 'TT1' for Locator, 'TT2' for TrustTrack.

        api_key: List[str]
            During the initialization of a web user, it will try to get a a list of api-keys
            from TrustTrack. If it's successful, it'll be listed in this attribute.
    """
    all = []

    def __init__(self, d: dict, locator: 'Locator', owner: 'Client'):
        self.all.append(self)
        self.locator = locator
        self.client = owner
        self.id = int(d['id_u'])
        self.company = d['company']
        self.username = d['username']
        self.count_objects = d['count_objects']

        if d['type'] == 'USER':
            self.is_admin = False
        else:
            self.is_admin = True

        self.login = d['login']
        self.phone = d['phone']
        self.email = d['email']
        self.source = d['source']
        self.link = f'{locator.HOST}/administrator/webusers/redirectAdmin?cmd=redirect_adminTT2&id={self.id}&is_tt2=1'
        self.api_key = self.get_api_keys()

    def get_api_keys(self) -> List[str]:
        api_key_req = self.locator.session.get(self.link)
        token = api_key_req.history[0].headers['Location']
        token = token.split('=')[1]
        headers = {'Authorization': token}
        api_key_req = self.locator.session.get('https://gtfrota.fm-track.com/gateway/user-service/v20181205/users/public-api-keys/', headers=headers)
        try:
            key = [i['id'] for i in api_key_req.json()['items']]
        except KeyError:
            key = []
        return key
        
    def __repr__(self) -> str:
        return f'[web id:{self.id}] {self.username}'