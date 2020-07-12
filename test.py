import sys
import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

ICCID = '89551805500000007882'

ARQIA_HOST = 'http://arqia.saitro.com'
ARQIA_LOGIN = 'estenio.benatti@excelbr.com.br'
ARQIA_PASS = 'd79d4'
ARQIA_iS = 'ODMyNQ=='

driver = webdriver.Chrome()
driver.get('http://arqia.saitro.com/')
driver.find_element_by_id('login').send_keys(ARQIA_LOGIN)
form = driver.find_element_by_id('senha')
form.send_keys(ARQIA_PASS)
form.send_keys(Keys.RETURN)
time.sleep(2)
print(driver.find_element_by_tag_name('h1').text)
driver.get('http://arqia.saitro.com/simcards/')
form = driver.find_element_by_id('vB')
form.send_keys(ICCID)
form.send_keys(Keys.RETURN)
soup = BeautifulSoup(driver.page_source)
phone = soup('td')[5].text