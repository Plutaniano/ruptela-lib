import requests
import colored
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from classes import *

# Locator
LOCATOR_HOST = 'http://track.ruptela.lt'
LOCATOR_LOGIN = 'ExcelProdutos'
LOCATOR_PASS = 'sLzN58LZ'
API_HOST = 'http://api.fm-track.com'
API_KEY = "Al-xrBlaeH-JXIj0RuPQT6FwuPFrZZGd"

class Locator:
    def __init__(self):
        self.login()
        if self.logged_in:
            self.clients = self.create_clients()
            self.hardwares = self.create_hardwares()

    def login(self):
        self.session = requests.Session()
        login_req = self.session.post(LOCATOR_HOST + '/administrator/authentication/login', {'sl': LOCATOR_LOGIN, 'ps': LOCATOR_PASS })
        if login_req.status_code != 200:
            self.logged_in = False
            print('Não foi possível logar no Locator.')
        else:
            self.logged_in = True
            print('Login OK!')
    
    def create_clients(self):
        headers = {'X-Requested-With': 'XMLHttpRequest'}
        clients_req = self.session.get(LOCATOR_HOST + '/administrator/clients/getList', headers=headers)
        for client in clients_req.json():
            client = Client(client, self)
            setattr(self, client.company, client)
        print(f'{len(Client.all)} clientes criados.')
        return Client.all         


    def create_objects(self):
        for client in self.clients:
            params = {
                "version": "1",
                "api_key": client.api_key,
            }
            obj_req = self.session.get(API_HOST + '/objects', params=params)
            for obj in obj_req.json():
                obj = Object(obj)
                client.objects.append(obj)
            print(f'{len(client.objects)} objetos criados para o cliente {client.company}.')

    def create_hardwares(self):
        params = {
            'cmd': 'edit',
            'nr': '626895'      # o que é 626895?
        }
        global hw_req
        hw_req = self.session.get(LOCATOR_HOST + '/administrator/objects/edit', params=params)
        soup = BeautifulSoup(hw_req.content, features='lxml')
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
        return f'[Locator] {len(self.clients)} clientes, {objs}'




def create_sim(phone, client, apn='m2m.arqia.br'):
    params = {
        'service_pr': 'Excel Produtos Eletronicos',
        'service_provider': '1407',
        'clients': str(client),         # 51879 = colorado
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
    r = s.post(HOST + '/administrator/connection/create', params)
    soup = BeautifulSoup(r.text, 'html.parser')
    try:
        string = color(soup('div', 'error')[0].contents[0], 'red', 'WHITE')
        success = False
    except:
        string = color('OK!', 'green', 'white')
        success = True
    print(f'create_SIM: {phone} * {string}')
    return success


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
        template_id='672',
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
        phone_id = _get_phone_id(phone)
    except:
        create_sim(phone, client)
        phone_id = _get_phone_id(phone)
    params = {
        'client': str(client),                  # Client ID - 51879=Colorado
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
        'hardware_id': hardwares[hardware][0],  # Hardware ID - FM Eco4 S=157
        'soft': hardwares[hardware][1],         # Soft ID
        'template_id': str(template_id),        # Template ID - Default 672 para EU**Standart**ECO4-S
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
    r = s.post(HOST + '/administrator/objects/create', params)
    check_status(r)
    soup = BeautifulSoup(r.text, 'html.parser')
    try:
        string = color(soup('div', 'error')[0].contents, 'red', 'WHITE')
        success = False
    except:
        string = color(soup('span', {'class': 'done'})[0].text, 'green', 'white')
        success = True
    print(f'[*] Criação do objeto: {name}')
    print(f'--- status {string}')
    return success


def color(msg, bg='RED', fg='WHITE'):
    bg = eval(f'colored.back.{bg.upper()}')
    fg = eval(f'colored.fore.{fg.upper()}')
    return f'{bg}{fg}{colored.style.BOLD}{msg}{colored.style.RESET}'


def _get_phone_id(phone):
    phone = str(phone)
    r = s.get(HOST + '/administrator/objects/edit', params={'cmd': 'edit', 'nr': '558737'})
    soup = BeautifulSoup(r.text, 'html.parser')
    for tag in soup.find(id='oconnection').find_all('option'):
        if tag.text == phone:
            return tag['value']
    else:
        raise Exception('Phone not found!')





def select_hardware():
    for i, hw in enumerate(hardwares):
        print(f'[ID:{i}] {hw}')
    print('\n\n')
    index = int(input('Selecione o ID do hardware a ser utilizado: '))
    return list(hardwares.keys())[index]



def check_status(http_req):
    if http_req.status_code != 200:
        print(f'URL: {http_req.url}')
        print(f'Status Code: {http_req.status_code}')
        print(f'Erro no pedido HTTP, objeto response na variavel req_debug')
        global req_debug
        req_debug = http_req
        raise Exception('HTTP request error')
    else:
        return True


hardwares = {
    # Nome:             (hardware_id, soft_id)
    'FM-Eco4':          (137, 308),
    'FM-Eco4 light':    (138, 315),
    'FM-Eco4 S':        (157, 356),
    'FM-Pro4':          (135, 306),
    'FM-Tco4':          (136, 307),
    'FM-Tco4-LCV':      (140, 321),
    'Plug4':            (139, 317)
}

if __name__ == '__main__':
    l = Locator()