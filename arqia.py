from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup

ARQIA_HOST = 'http://arqia.saitro.com'
ARQIA_LOGIN = 'estenio.benatti@excelbr.com.br'
ARQIA_PASS = 'd79d4'
ARQIA_iS = 'ODMyNQ=='

# options
options = Options()
options.headless = True
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# Criando browser e logando
driver = webdriver.Chrome(options=options)
driver.get(ARQIA_HOST)
driver.find_element_by_id('login').send_keys(ARQIA_LOGIN)
form = driver.find_element_by_id('senha')
form.send_keys(ARQIA_PASS)
form.send_keys(Keys.RETURN)
time.sleep(2)
print(driver.find_element_by_tag_name('h1').text)

def ICCID_to_phone(ICCID):
    driver.get(ARQIA_HOST + '/simcards/')
    form = driver.find_element_by_id('vB')
    form.send_keys(ICCID)
    form.send_keys(Keys.RETURN)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    phone = soup('td')[5].text
    return phone