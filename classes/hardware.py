from __future__ import annotations

from bs4 import BeautifulSoup


class MetaHardware(type):
    all = []
    _is_init = False
    
    @classmethod
    def init(cls, locator):
        params = {
            'cmd': 'edit',
            'nr': '626895'      # o que é 626895?
        }
        hw_req = locator.session.get(locator.HOST + '/administrator/objects/edit', params=params)
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
        cls._is_init = True
        cls.all = hardwares

    def __getitem__(self, key):
        for hardware in Hardware.all:
            if hardware.name == key:
                return hardware
        raise KeyError(f'Não foi possível encontrar um hardware com o nome \'{key}\'.')

    def __repr__(self):
        return f'[Hardwares] <hardwares:{len(self.all)} init:{self._is_init}>'


class Hardware(metaclass=MetaHardware):
    all = MetaHardware.all

    def __init__(self, d):
        self.all.append(self)
        self.id = d['id']
        self.name = d['name']
        self.description = d['description']
        self.hw_version = d['hw_version']
        self.soft_id = d['soft_id']
        self.soft_version = d['soft_version']

    def __repr__(self):
        return f'[HW] {self.name}'
    
    @classmethod
    def init(cls, locator) -> None:
        MetaHardware.init(locator)