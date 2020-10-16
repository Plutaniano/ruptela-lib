import os
import atexit

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from .sim_card import Sim_Card

class Operator:
    """
    Class for gathering data from operator's website and storing it in a
    standard format. Also provides some default search methods.
    """

    all = []

    def __init__(self, name: str, username: str, password: str, host: str, apn: tuple) -> None:
        Operator.all.append(self)

        self.name = name
        self.username = username
        self.password = password
        self.host = host
        self.apn = apn

        self.set_options()
        self.create_webdriver()
    

    def login(self) -> None:
        # this function needs to be implemented on classes that inherit from Operator
        pass
        
    def sync_simcards(self) -> None:
        # this function needs to be implemented on classes that inherit from Operator
        pass
    
    def create_webdriver(self) -> None:
        """
        Creates a webdriver instance on self.driver.
        """
        manager = ChromeDriverManager(log_level='0').install()
        self.driver = webdriver.Chrome(manager, options=self.options)
        self.driver.keys = Keys

    def set_options(self) -> None:
        """
        Configures some options and settings for the webdriver.
        """
        options = Options()
        options.headless = True
        prefs = {"download.default_directory" : os.getcwd()}
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option("prefs",prefs)
        self.options = options

    def find_by_ICCID(self, ICCID) -> Sim_Card:
        """
        Returns a sim card with the provided ICCID. If it can't be found,
        it raises KeyError instead.
        """
        for sim in self.simcards:
            if sim.ICCID == ICCID:
                return sim
        raise KeyError(f'O ICCID {ICCID} não corresponde a um número.')

    def find_by_line(self, line) -> Sim_Card:
        """
        Returns a sim card with the provided phone number (line). If it
        can't be found, it raises KeyError instead.
        """
        for sim in self.simcards:
            if sim.line == line:
                return sim
        raise KeyError(f'Não foi possível encontrar um sim card com a linha {line}')

    def __repr__(self):
        return f'[{self.name}] {len(self.simcards)} sim cards.'

    @atexit.register
    def _exit_handler(self) -> None:
        """
        Closes the webdriver instance on program close, prevents memory leaks.
        """
        self.driver.quit()