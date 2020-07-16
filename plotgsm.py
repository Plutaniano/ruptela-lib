import requests
import datetime as dt
import matplotlib.pyplot as plt
from locator import Locator
from arqia import Arqia


l = Locator()



timefrom = float(input('time from?'))
timeto = float(input('time to?'))
#timefrom = (dt.datetime.utcnow() - dt.timedelta(days=x)).isoformat()[:-3] + "Z"
#timeto = (dt.datetime.utcnow() - dt.timedelta(days=y)).isoformat()[:-3] + 'Z'

packets = []
for obj in l.Colorado.objects:
    for p in obj.get_interval(timefrom, timeto):
        packets.append(p)

lat = []
lon = []
gsm = []

for p in packets:
    lat.append(p["position"]["latitude"])
    lon.append(p["position"]["longitude"])
    try:
        gsm.append(min(p["inputs"]["device_inputs"]["gsm_signal_strength"], 31))
    except:
        print('erro')
        gsm.append(0)
plt.scatter(lon, lat, c=gsm, cmap='binary')
plt.suptitle(f'{timefrom} até {timeto}')
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
