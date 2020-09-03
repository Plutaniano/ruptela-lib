import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

from .client import Client
from .object import Object
from .hardware import Hardware


# Locator

class Locator():
    HOST = 'http://track.ruptela.lt'
    API_HOST = 'http://api.fm-track.com'

    def __init__(self, username='ExcelProdutos', password='sLzN58LZ'):
        self.username = username
        self.password = password
        self.login()
        if self.logged_in:
            print('--->\t Coletando informações, por favor aguarde...')
            self.clients = self.create_clients()
            self.hardwares = self.create_hardwares()

    def login(self):
        self.session = requests.Session()
        login_req = self.session.post(self.HOST + '/administrator/authentication/login', {'sl': self.username, 'ps': self.password })
        if login_req.status_code != 200:
            self.logged_in = False
            print('[ERR]\t Não foi possível logar no Locator.')
        else:
            self.logged_in = True
            print('--->\t Login OK!')
    
    def create_clients(self):
        headers = {'X-Requested-With': 'XMLHttpRequest'}
        clients_req = self.session.get(self.HOST + '/administrator/clients/getList', headers=headers)
        for client in clients_req.json():
            client = Client(client, self)
            setattr(self, client.company.replace(' ', '_'), client)
        print(f'--->\t {len(Client.all)} clientes criados.')
        return Client.all         


    def create_objects(self):
        for client in self.clients:
            params = {
                "version": "1",
                "api_key": client.api_key,
            }
            obj_req = self.session.get(self.HOST + '/objects', params=params)
            for obj in obj_req.json():
                obj = Object(obj)
                client.objects.append(obj)
            print(f'{len(client.objects)} objetos criados para o cliente {client.company}.')


    def create_hardwares(self):
        params = {
            'cmd': 'edit',
            'nr': '626895'      # o que é 626895?
        }
        hw_req = self.session.get(self.HOST + '/administrator/objects/edit', params=params)
        soup = BeautifulSoup(hw_req.content, 'html.parser')
        rows = soup.find('div', id='hardwarelist').find('table').find_all('tr')
        hardwares = []
        for tr in rows[1:]:
            tds = tr.find_all('td')
            d = {}
            d['id'] = tds[0].text
            d['name'] = tds[1].text
            d['description'] = tds[2].text
            d['hw_version'] = tds[3].text
            d['soft_id'] = tds[4].text.split(';')[0][4:]
            d['soft_version'] = tds[4].text.split(';')[1][41:-2]
            hardwares.append(Hardware(d))
        return hardwares

    
    def __repr__(self):
        objs = 0
        for client in self.clients:
            objs += len(client.objects)
        return f'[Locator] {len(self.clients)} clientes, {objs} objetos'


    def _get_phone_id(self, phone):
        phone = str(phone)
        headers = {
            'Connection': 'keep-alive',
            'Accept': 'application/javascript, application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-Range': 'items=0-999',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.173',
            'Range': 'items=0-999',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'http://track.ruptela.lt/administrator/connection',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        }
        r = self.session.get(self.HOST + '/administrator/connection/getList', headers=headers)
        for row in r.json():
            if row['phone'] == phone:
                return row['id'].strip()
        else:
            raise Exception('Phone not found!')

    def create_new_object(
        self,
        name,
        imei,
        hardware,
        phone,
        client,
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
        username='',
        password='',
        ):
        try:
            phone_id = self._get_phone_id(phone, client)
        except:
            self.create_sim(phone, client)
            phone_id = self._get_phone_id(phone)
        params = {
            'client': str(client.id),               # Client ID - 51879=Colorado
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
            'payment_plan_id': str(ppid),           # Payment Plan ID - default 'Demo'=2911
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
            'username': str(username),              # FM Login
            'password': str(password),              # FM Password
            'create': 'Create',                     # Create
        }
        print(f'[ * ] Criando objeto no Locator.')
        print(f'--->\t Nome: {str(name)}, cliente: {client.company}')
        r = self.session.post(self.HOST + '/administrator/objects/create', params)
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


    def create_sim(self, phone, client, apn='m2m.arqia.br'):
        print('[ * ] Criando SIM card no Locator.')
        print(f'--->\t Telefone: {phone}')
        print(f'--->\t Cliente: {client.company}')
        params = {
            'service_pr': 'Excel Produtos Eletronicos',
            'service_provider': '1407',
            'clients': str(client.id),
            'provider': '30',
            'phone': str(phone),
            'numbers': '1',
            'pin': '',
            'puk': '',
            'imsi': '',
            'ip': '',
            'apn': str(apn),
            'login': '',
            'password': '',
            'create': 'Create'
        }
        
        r = self.session.post(self.HOST + '/administrator/connection/create', params)
        soup = BeautifulSoup(r.text, 'html.parser')
        try:
            string = soup('div', 'error')[0].contents[0]
            success = False
        except:
            string = 'OK!'
            success = True
        print(f'--->\t status: {string}\n')
        return success


if __name__ == '__main__':
    l = Locator()
