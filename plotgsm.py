import requests
import datetime as dt
import matplotlib.pyplot as plt


KEY = "Al-xrBlaeH-JXIj0RuPQT6FwuPFrZZGd"


# frota = input("digite o número de frota: ")
ids = []
nomes = []
r = requests.get("http://api.fm-track.com/objects", params={"version": "1", "api_key": KEY})
for i in r.json():
    ids.append(i["id"])
    nomes.append(i["name"])

x = float(input('time from?'))
y = float(input('time to?'))
timefrom = (dt.datetime.utcnow() - dt.timedelta(days=x)).isoformat()[:-3] + "Z"
timeto = (dt.datetime.utcnow() - dt.timedelta(days=y)).isoformat()[:-3] + 'Z'
pacotes = []
for id in ids:
    print(f'[*] Carro[{ids.index(id)+1}/{len(ids)}] adquirindo dados nome: {nomes[ids.index(id)]} id:{id}')
    r = requests.get(f'http://api.fm-track.com/objects/{id}/coordinates', params={'version': "2", "api_key": KEY, 'from_datetime': timefrom, 'to_datetime': timeto, 'limit': 1000})
    pacotes = pacotes + r.json()["items"]
    try:
        token = r.json()['continuation_token']
        while token:
            token = r.json()['continuation_token']
            print(f"[**] adquirindo mais dados token:{token}")
            r = requests.get(f'http://api.fm-track.com/objects/{id}/coordinates', params={'version': "2", "api_key": KEY, 'from_datetime': r.json()['continuation_token'], 'to_datetime': timeto, 'limit': 1000})
            pacotes = r.json()["items"] + pacotes
    except KeyError:
        print("[**] fim dos dados")

lat = []
lon = []
gsm = []

for p in pacotes:
    lat.append(p["position"]["latitude"])
    lon.append(p["position"]["longitude"])
    try:
        gsm.append(min(p["inputs"]["device_inputs"]["gsm_signal_strength"], 31) / 31)
    except:
        print('erro')
        gsm.append(0)
plt.scatter(lon, lat, c=gsm, cmap='binary')
plt.suptitle(f'{timefrom[:-14]} até {timeto[:-14]}')
plt.annotate('colorado', (-48.191086, -20.276510))
plt.annotate('Ribeirão', (-47.812909, -21.165933))
plt.annotate('guaira', (-48.311234, -20.324409))
plt.annotate('goiania', (-49.266578, -16.693758))
plt.xlim(-50, -45.5)
plt.ylim(-23, -18)
ax = plt.gca()
ax.set_facecolor('xkcd:salmon')
plt.colorbar()
plt.show()
