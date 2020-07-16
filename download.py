# downloadfile

import requests

cookies = {
    'PHPSESSID': 'fog9gt1fmhuplksut1cr2nvhj2',
}

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'Origin': 'http://arqia.saitro.com',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.173',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Referer': 'http://arqia.saitro.com/relatorios/',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
}

data = {
  'iS': 'ODMyNQ=='
}

response = requests.post('http://arqia.saitro.com/relatorios/simcard/simcard.php', headers=headers, cookies=cookies, data=data, verify=False)
