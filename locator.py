from datetime import datetime, timedelta
import requests
import colored
from bs4 import BeautifulSoup
from classes import *


HOST = 'http://track.ruptela.lt'
LOGIN = 'ExcelProdutos'
PASS = 'sLzN58LZ'


s = requests.Session()

login_dict = {
    'sl': LOGIN,
    'ps': PASS
}

r = s.post(HOST + '/administrator/authentication/login', login_dict)
print(r)


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
        string = color(soup('div', 'error')[0].contents, 'red', 'WHITE')
        success = False
    except:
        string = color('OK!', 'green', 'white')
        success = True
    print(f'create_SIM: {phone} * {string}')
    return success


def create_object(
        name,
        imei,
        hardware,
        phone,
        client,
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
        phone_id = get_phone_id(phone)
    except:
        create_sim(phone, client)
        phone_id = get_phone_id(phone)
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
    soup = BeautifulSoup(r.text, 'html.parser')
    try:
        string = color(soup('div', 'error')[0].contents, 'red', 'WHITE')
        success = False
    except:
        string = color(soup('span', {'class': 'done'})[0].text, 'green', 'white')
        success = True
    print(f'create_object: {name} * {string}')
    return success


def color(msg, bg='RED', fg='WHITE'):
    bg = eval(f'colored.back.{bg.upper()}')
    fg = eval(f'colored.fore.{fg.upper()}')
    return f'{bg}{fg}{colored.style.BOLD}{msg}{colored.style.RESET}'


def get_phone_id(phone):
    phone = str(phone)
    r = s.get(HOST + '/administrator/objects/edit', params={'cmd': 'edit', 'nr': '558737'})
    soup = BeautifulSoup(r.text)
    for tag in soup.find(id='oconnection').find_all('option'):
        if tag.text == phone:
            return tag['value']
    else:
        raise Exception('Phone not found!')


def create_clients():
    print('Obtendo clientes...')
    r = s.get(HOST+'/administrator/clients/getList', headers=REQUEST_HEADERS)
    for client in r.json():
        Client(client)



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

REQUEST_HEADERS = {
    'Connection': 'keep-alive',
    'Accept': 'application/javascript, application/json',
    'X-Requested-With': 'XMLHttpRequest',
    'X-Range': 'items=0-999',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.173',
    'Range': 'items=0-999',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': 'http://track.ruptela.lt/administrator/clients',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
}