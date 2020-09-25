import os
import atexit

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from .sim_card import Sim_Card

class Operator:
    all = []

    def __init__(self, name: str, username: str, password: str, host: str, apn: tuple):
        Operator.all.append(self)
        atexit.register(self._exit_handler)

        self.name = name
        self.username = username
        self.password = password
        self.host = host
        self.apn = apn

        self.set_options()
        self.create_webdriver()
    

    def login(self) -> None:
        # implementar função
        pass
        
    def sync_simcards(self) -> None:
        # implementar função
        pass
    
    def create_webdriver(self) -> None:
        manager = ChromeDriverManager(log_level='0').install()
        self.driver = webdriver.Chrome(manager, options=self.options)
        self.driver.keys = Keys

    def set_options(self) -> None:      #define algumas opções para o browser "virtual"
        options = Options()
        options.headless = True
        prefs = {"download.default_directory" : os.getcwd()}
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option("prefs",prefs)
        self.options = options

    def find_by_ICCID(self, ICCID) -> Sim_Card:     # retorna o objeto Sim_Card correspondente ao ICCID inputado
        for sim in self.simcards:
            if sim.ICCID == ICCID:
                return sim
        raise KeyError(f'O ICCID {ICCID} não corresponde a um número.')

    def find_by_line(self, line) -> Sim_Card:
        for sim in self.simcards:
            if sim.line == line:
                return sim
        raise KeyError(f'Não foi possível encontrar um sim card com a linha {line}')

    def __repr__(self):
        return f'[{self.name}] {len(self.simcards)} sim cards.'

    def _exit_handler(self):
        self.driver.quit()