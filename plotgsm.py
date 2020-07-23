import requests
import datetime as dt
import matplotlib.pyplot as plt
from locator import Locator
from arqia import Arqia


carros = ['228254']

print(f'Lista de carros: {", ".join(carros)}')
timefrom = float(input('time from?'))
timeto = float(input('time to?'))
timefromtitle = (dt.datetime.utcnow() - dt.timedelta(days=timefrom)).isoformat()[:-16]
timetotitle = (dt.datetime.utcnow() - dt.timedelta(days=timeto)).isoformat()[:-16]

l = Locator()
packets = []

for obj in l.Colorado.objects:
    if obj.name in carros:
        for p in obj.get_interval(timefrom, timeto):
            packets.append(p)

lat = []
lon = []
gsm = []

for p in packets:
    lon.append(p.position["longitude"])
    lat.append(p.position["latitude"])
    try:
        gsm.append(min(p.gsm_signal_strength, 31))
    except:
        print('erro')
        gsm.append(0)
        
plt.scatter(lon, lat, c=gsm, cmap='binary')
plt.suptitle(f'{timefromtitle} até {timetotitle}')
plt.annotate('colorado', (-48.191086, -20.276510))
plt.annotate('Ribeirão', (-47.812909, -21.165933))
plt.annotate('guaira', (-48.311234, -20.324409))
plt.annotate('goiania', (-49.266578, -16.693758))
plt.xlim(-50, -45.5)
plt.ylim(-23, -18)
ax = plt.gca()
ax.set_facecolor('xkcd:salmon')
plt.colorbar()
print('Mostrando gráfico...')
plt.show()


def setaxis(xmin, xmax, ymin, ymax):
    if xmax - xmin > ymax - ymin:
        axisrange = xmax-xmin
        midpoint_x = (xmax - xmin)/2
        midpoint_y = (ymax - ymin)/2
        


