from __future__ import annotations
import requests
from typing import *
from datetime import datetime, timedelta

from bs4 import BeautifulSoup

from .web_user import Web_User
from .object import Object

class Client:
    all = []

    def __init__(self, d: dict, locator: 'Locator'):
        self.index = len(Client.all)
        self.all.append(self)
        self.locator = locator
        
        self.company = d['company']
        self.phone = d['phone']
        self.id = d['id']
        self.address = d['address']
        self.email = d['email']
        self.objects = []

        self.get_web_users(sync=True)
        self.get_objects(sync=True)
        print(f'--->\t\t \'{self.company}\' criado com {len(self.objects)} objetos.')

    def __repr__(self):
        return f'[Client] <company:{self.company} objects:{len(self.objects)}>'

    def get_web_users(self, sync: bool = False) -> Union[List[Web_User], None]:
        headers = {'X-Requested-With': 'XMLHttpRequest'}
        web_req = self.locator.session.get(self.locator.HOST + '/administrator/webusers/getList', headers=headers)
        web_users = []
        for user in web_req.json():
            if user['company'] == self.company:
                web_user = Web_User(user, self.locator, self)
                setattr(self, web_user.login, web_user)
                web_users.append(web_user)
        if sync:
            self.web_users = web_users
        else:
            return web_users
    
    def get_objects(self, sync: bool = False) -> Union[None, List[Object]]:
        params={
            "version": "1",
            "api_key": self.api_key
        }
        objs_req = requests.get("http://api.fm-track.com/objects", params=params)
        objs = []
        for obj in objs_req.json():
            objs.append(Object(obj, self))
        if sync:
            self.objects = objs
        else:
            return objs

    def find_by_name(self, name: str) -> Object:
        for i in self.objects:
            if i.name == name:
                return i
        raise NameError('Não foi possível encontrar objeto com o nome especificado.')

    def create_new_object(
        self,
        name,
        imei,
        hardware,
        phone,
        description='.',
        drivers_phone='',
        serial='',
        template_id='2531',
        delay_hour='00',
        delay_min='30',
        make='',
        model='',
        object_color='',
        notes='',
        vin='',
        vehicle_type='UNSPECIFIED',
        tppid='',
        ppid='2911',
        installer='',
        fm_username='',
        fm_password='',
        apn='voxter.br',
        apn_login='algar',
        apn_password='algar'
        ):
        try:
            phone_id = self.locator._get_phone_id(phone)
        except:
            self.create_sim(phone, apn, apn_login, apn_password)
            phone_id = self.locator._get_phone_id(phone)
        params = {
            'client': str(self.id),               # Client ID - 51879=Colorado
            'object': str(name),                    # Object Name
            'type': 'vehicle',                      # vehicle or trailer
            'state': '1',                           # State: 1-'' 2-'New/not installed' 3-Testing 4-For Repair 5-Uninstalled
            'tt_version': 'TT2',                    # TT2
            'description': str(description),        # Obj Description
            'connection': str(phone_id),            # Phone Number
            'phone': str(drivers_phone),            # Drivers phone
            'serial': str(serial),                  # Serial Number
            'imei': str(imei),                      # IMEI
            'hardware': str(hardware),              # Hardware - ex: 'FM-Eco4 S'
            'hardware_id': hardware.id,             # Hardware ID - FM Eco4 S=157
            'soft': hardware.soft_id,               # Soft ID
            'template_id': str(template_id),        # Template ID - Default 2531 para "GTFrota Eco Light"
            'delay_hour': str(delay_hour),          # Delay hour
            'delay_min': str(delay_min),            # Delay minutes
            'make': str(make),                      # Make
            'model': str(model),                    # Model
            'object_color': str(object_color),      # Color
            'admin_notes': str(notes),              # Notes
            'vin': str(vin),                        # VIN
            'vehicle_type': str(vehicle_type),      # Vehicle Type - UNSPECIFIED or PASSENGER
            'temp_payment_plan_id': str(tppid),     # Temporary Payment Plan
            'temp_from_date': datetime.today().strftime('%Y-%m-%d'),
            'temp_to_date': (datetime.today() + timedelta(days=30)).strftime('%Y-%m-%d'),
            'payment_plan_id': str(ppid),           # Payment Plan ID - default 'TrustTrack2 Standart' = 3237
            'enforce_disable_payment_plan': '0',    # Enforce disable payment plant
            'preselected_payment_plan': '',         # Preselected payment plan
            'installer': str(installer),            # Installer
            'install_date': '',                     # Install date
            'uninstall_date': '',                   # Uninstall date
            'visible': '0',                         # Visible
            'include_web_service': '1',             # Include in web service
            'trailer_id': '',                       # Trailer ID
            'monitor_enabled': '0',                 # Monitor enabled
            'mask': '',                             # Mask
            'extra_mask': '',                       # Extra mask
            'pnd_type': '0',                        # PND Type
            'username': str(fm_username),           # FM Login
            'password': str(fm_password),           # FM Password
            'create': 'Create',                     # Create
        }
        print(f'[ * ] Criando objeto no Locator.')
        print(f'--->\t Nome: {str(name)}, cliente: {self.company}')
        r = self.locator.session.post(self.locator.HOST + '/administrator/objects/create', params)
        soup = BeautifulSoup(r.text, 'html.parser')
        try:
            string = soup('div', 'error')[0].contents
            success = False
        except:
            string = soup('span', {'class': 'done'})[0].text
            if string == 'Done':
                string = 'OK!'
            success = True

        print(f'--->\t status: {string}\n')
        if string != 'OK!':
            print('--->\t Algo de errado ocorreu, enviando informações sobre erro para a engenharia.')
        return success
    
    def create_sim(self, phone, apn, login='', password=''):
        print('[ * ] Criando SIM card no Locator.')
        print(f'--->\t Telefone: {phone}')
        print(f'--->\t Cliente: {self.company}')
        params = {
            'service_pr': 'Excel Produtos Eletronicos',
            'service_provider': '1407',
            'clients': str(self.id),
            'provider': '30',
            'phone': str(phone),
            'numbers': '1',
            'pin': '',
            'puk': '',
            'imsi': '',
            'ip': '',
            'apn': str(apn),
            'login': str(login),
            'password': str(password),
            'create': 'Create'
        }
        
        r = self.locator.session.post(self.locator.HOST + '/administrator/connection/create', params)
        soup = BeautifulSoup(r.text, 'html.parser')
        try:
            string = soup('div', 'error')[0].contents[0]
            success = False
        except:
            string = 'OK!'
            success = True
        print(f'--->\t status: {string}\n')
        return success



    @property
    def api_key(self) -> str:
        for web_user in self.web_users:
            try:
                return web_user.api_key
            except:
                pass
        raise Exception('Não foi possível encontrar uma api key devido a falta de web users ou falta de api nos web users.')        