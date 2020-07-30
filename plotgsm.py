import datetime as dt
from math import ceil, sqrt
import matplotlib.pyplot as plt
from locator import Locator
from arqia import Arqia
from classes import Object
from collections import Counter

# timefromtitle = (dt.datetime.utcnow() - dt.timedelta(days=timefrom)).isoformat()[:-16]
# timetotitle = (dt.datetime.utcnow() - dt.timedelta(days=timeto)).isoformat()[:-16]

# plt.scatter(lon, lat, c=gsm, cmap='binary', label='dddd')
# plt.suptitle(f'{timefromtitle} até {timetotitle}')
# plt.annotate('colorado', (-48.191086, -20.276510))
# plt.annotate('Ribeirão', (-47.812909, -21.165933))
# plt.annotate('guaira', (-48.311234, -20.324409))
# plt.annotate('goiania', (-49.266578, -16.693758))
# plt.xlim(-50, -45.5)
# plt.ylim(-23, -18)
# ax = plt.gca()
# ax.set_facecolor('xkcd:salmon')
# plt.colorbar()
# print('Mostrando gráfico...')
# plt.show()

def plot_gsm(objs, timefrom, timeto=0, s=None):
    fig = plt.figure()

    if isinstance(objs, (str, Object)):
        objs = [objs]
    
    lat = []
    lon = []
    gsm = []
    for obj in objs:
        packets = obj.get_interval(timefrom, timeto)

        for p in packets:
            lon.append(p.position["longitude"])
            lat.append(p.position["latitude"])
            if p.gsm_signal_strength in [None, 255] :
                gsm.append(0)
            else:
                gsm.append(p.gsm_signal_strength)

    bar_ax = plt.subplot2grid((9,9), (8,0), colspan=9)
    c = Counter(gsm)
    bar_ax.bar(c.keys(), c.values())

    scatter_ax = plt.subplot2grid((9,9), (0,0), colspan=9, rowspan=8)
    scatter_ax.scatter(lon, lat, c=gsm, s=s, cmap='binary', label=obj.name)

    xspan = scatter_ax.get_xlim()[1] - scatter_ax.get_xlim()[0]
    yspan = scatter_ax.get_ylim()[1] - scatter_ax.get_ylim()[0]
    if xspan > yspan:
        midpoint = sum(scatter_ax.get_ylim())/2
        scatter_ax.set_ylim(midpoint - xspan/2, midpoint + xspan/2)
    else:
        midpoint = sum(scatter_ax.get_xlim())/2
        scatter_ax.set_xlim(midpoint - yspan/2, midpoint + yspan/2)

    print(f'xlim: {scatter_ax.get_xlim()}, ylim: {scatter_ax.get_ylim()}')
    input('?')
    img = plt.imread('img.png')
    ext = [scatter_ax.get_xlim()[0],scatter_ax.get_xlim()[1],scatter_ax.get_ylim()[0],scatter_ax.get_ylim()[1]]
    scatter_ax.imshow(img, extent=ext)
    plt.tight_layout()
    plt.show()  


if __name__ == '__main__':
    l = Locator()
    