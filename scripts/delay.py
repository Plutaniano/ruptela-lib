from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import requests

d = webdriver.Chrome(ChromeDriverManager().install())

h = 'https://track.ruptela.lt'
js = '''
	document.querySelector("#delay_hour").value = 0;
	document.querySelector("#delay_min").value = 5; 
	document.querySelector("#save_button").click();
	'''
s = requests.Session()

headers = {
    'Connection': 'keep-alive',
    'Accept': 'application/javascript, application/json',
    'X-Requested-With': 'XMLHttpRequest',
    'X-Range': 'items=0-999',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
    'Range': 'items=0-999',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://track.ruptela.lt/administrator/objects',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
}

s.post(h + '/administrator/authentication/login', 
	params={'page':'authentication', 'action':'login'}, 
	data={'sl':'ExcelProdutos', 'ps':'sLzN58LZ'}
	)

r = s.get(h + '/administrator/objects/getList',
	params = (
    ('object_description', ''),
    ('object_name', ''),
    ('company_name', 'Colorado'),
    ('phone', ''),
    ('imei', ''),
    ('serial', ''),
    ('hardware', 'FM-Eco4 S'),
    ('objectId', ''),
    ('vin', ''),
    ('tt_version', ''),
    ('tt2_object_id', ''),
	),
	headers=headers
)

links = [obj['view'].split('"')[1] for obj in r.json()]


def change_delay(driver, delay, links):
	for i in links:
		driver.get(h + i)
		driver.execute_script(js)
		try:
			driver.switch_to.alert.dismiss()
		except:
			pass
		print(i)
