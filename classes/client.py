from __future__ import annotations
import requests
from typing import *
from datetime import datetime, timedelta

from bs4 import BeautifulSoup

from .web_user import Web_User
from .object import Object
from .sim_card import Sim_Card

import logging
logger = logging.getLogger(__name__)

class Client:
    """
    Class for storing data related to locator clients.
    
    ...

    Attributes:
    

    """
    all = []

    def __init__(self, d: dict, locator: 'Locator') -> None:
        self.index = len(Client.all)
        self.all.append(self)
        self.locator = locator
        
        self.company = d['company']
        self.phone = d['phone']
        self.id = d['id']
        self.address = d['address']
        self.email = d['email']
        self.objects = []
        self.web_users = []

        if locator.is_fast == False:
            self.get_web_users(sync=True)
            self.get_objects(sync=True)

        logger.info(f'\'{self.company}\' criado com {len(self.objects)} objetos.')


    def get_web_users(self, sync: bool = False) -> Union[List[Web_User], None]:
        """
        Gathers data from all web users associated with this client. If sync=True is passed,
        self.web_users is set to a list of all Web_Users, otherwise, it returns a list of
        those web users.
        """

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
    
    def get_objects(self, sync: bool = False) -> Union[List[Object], None]:
        """
        Gathers data from all objects associated with this client. If sync=True is passed,
        self.objects is set to a list of all objects, otherwise, it returns a list of those objects.
        """
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
        """
        Returns a object with the provided name. Raises NameError if it doesn't exist.
        """
        for i in self.objects:
            if i.name == name:
                return i
        raise NameError('Não foi possível encontrar objeto com o nome especificado.')

    def create_new_object(self, name: str, **kwargs: str) -> str:
        """
        
        """
        d = {
        'hardware': '',
        'description': '.',
        'drivers_phone': '',
        'serial': '',
        'template_id': '2531', # GTFrota Ecolight template
        'delay_hour': '00',
        'delay_min': '30',
        'make': '',
        'model': '',
        'object_color': '',
        'notes': '',
        'vin': '',
        'vehicle_type': 'UNSPECIFIED',
        'tppid': '',
        'ppid': '2911',
        'installer': '',
        'fm_username': '',
        'fm_password': ''            
        }
        d.update(kwargs)

        if 'device' in d.keys():
            d['imei'] = d['device'].imei
            d['hardware'] = d['device'].hardwarelist['name']
            d['hardware_id'] = d['device'].hardwarelist['id']
            d['soft_id'] = d['device'].hardwarelist['soft_id']

        try:
            assert d['name'] != '' and isinstance(d['name'], str)
        except AssertionError:
            raise KeyError('Invalid name')


        try:
            phone_id = self.locator._get_phone_id(d['sim_card'])
        except:
            self.create_sim(d['sim_card'])
            phone_id = self.locator._get_phone_id(d['sim_card'])
        params = {
            'client': str(self.id),                      # Client ID - 51879=Colorado
            'object': str(name),                         # Object Name
            'type': 'vehicle',                           # vehicle or trailer
            'state': '1',                                # State: 1-'' 2-'New/not installed' 3-Testing 4-For Repair 5-Uninstalled
            'tt_version': 'TT2',                         # TT2
            'description': str(d['description']),        # Obj Description
            'connection': str(phone_id),                 # Phone Number
            'phone': str(d['drivers_phone']),            # Drivers phone
            'serial': str(d['serial']),                  # Serial Number
            'imei': str(d['imei']),                      # IMEI
            'hardware': str(d['hardware']),              # Hardware - ex: 'FM-Eco4 S'
            'hardware_id': d['hardware_id'],             # Hardware ID - FM Eco4 S=157
            'soft': d['soft_id'],                        # Soft ID
            'template_id': str(d['template_id']),        # Template ID - Default 2531 para "GTFrota Eco Light"
            'delay_hour': str(d['delay_hour']),          # Delay hour
            'delay_min': str(d['delay_min']),            # Delay minutes
            'make': str(d['make']),                      # Make
            'model': str(d['model']),                    # Model
            'object_color': str(d['object_color']),      # Color
            'admin_notes': str(d['notes']),              # Notes
            'vin': str(d['vin']),                        # VIN
            'vehicle_type': str(d['vehicle_type']),      # Vehicle Type - UNSPECIFIED or PASSENGER
            'temp_payment_plan_id': str(d['tppid']),     # Temporary Payment Plan
            'temp_from_date': datetime.today().strftime('%Y-%m-%d'),
            'temp_to_date': (datetime.today() + timedelta(days=30)).strftime('%Y-%m-%d'),
            'payment_plan_id': str(d['ppid']),           # Payment Plan ID - default 'TrustTrack2 Standart' = 3237
            'enforce_disable_payment_plan': '0',    # Enforce disable payment plant
            'preselected_payment_plan': '',         # Preselected payment plan
            'installer': str(d['installer']),       # Installer
            'install_date': '',                     # Install date
            'uninstall_date': '',                   # Uninstall date
            'visible': '0',                         # Visible
            'include_web_service': '1',             # Include in web service
            'trailer_id': '',                       # Trailer ID
            'monitor_enabled': '0',                 # Monitor enabled
            'mask': '',                             # Mask
            'extra_mask': '',                       # Extra mask
            'pnd_type': '0',                        # PND Type
            'username': str(d['fm_username']),           # FM Login
            'password': str(d['fm_password']),           # FM Password
            'create': 'Create',                     # Create
        }
        logger.info(f'Criando objeto no locator. <name:{str(name)}, client: {self.company}>')
        r = self.locator.session.post(self.locator.HOST + '/administrator/objects/create', params)
        soup = BeautifulSoup(r.text, 'html.parser')
        error_strings = [i.text for i in soup('div', 'error')]

        if len(error_strings) > 0:
            raise Exception(' | '.join(error_strings))

        string = soup('span', {'class': 'done'})[0].text
        if string == 'Done':
            return 
        

    def create_sim(self, sim_card: Sim_Card) -> None:
        logger.info(f'Criando SIM card no Locator. <tel: {sim_card.line}, client: {self.company}')
        params = {
            'service_pr': str(self.locator.service_pr),
            'service_provider': str(self.locator.service_provider),
            'clients': str(self.id),
            'provider': '30',           # Provider: Other
            'phone': str(sim_card.line),
            'numbers': '1',
            'pin': '',
            'puk': '',
            'imsi': '',
            'ip': '',
            'apn': str(sim_card.operator.apn[0]),
            'login': str(sim_card.operator.apn[1]),
            'password': str(sim_card.operator.apn[2]),
            'create': 'Create'
        }
        
        r = self.locator.session.post(self.locator.HOST + '/administrator/connection/create', params)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        if len(soup('div', 'error')) > 0:
            raise Exception(soup('div', 'error'))

    @property
    def api_key(self) -> str:
        """
        Property that returns the first api-key avaiable in this client's webusers.
        Raise an exception if it finds None.
        """
        for web_user in self.web_users:
            try:
                return web_user.api_key
            except:
                pass
        raise Exception('Não foi possível encontrar uma api key devido a falta de web users ou falta de api nos web users.')

    def __repr__(self) -> str:
        return f'[Client] <company:\'{self.company}\', objects:{len(self.objects)}>'