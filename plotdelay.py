import matplotlib
import matplotlib.pyplot as plt
from classes import *

create_all_objects()

timefrom = float(input('time from? '))

for i in Object.all:
    i.packets = [Packet(p, i) for p in i.get_interval(timefrom)]
    print(f'[{i.name}] {len(i.packets)} pacotes')
    i.dates = []
    i.delays = []
    if len(i.packets) == 0:
        print('descartado')
        continue
    for p in range(1,len(i.packets)):
        packetdatetime = i.packets[p].datetime
        packetdelay = (i.packets[p].datetime - i.packets[p-1].datetime).total_seconds()
        i.dates.append(packetdatetime)
        i.delays.append(packetdelay)


objs_to_be_plotted = []
for i in Object.all:
    if len(i.delays) > 0:
        objs_to_be_plotted.append(i)


hfmt = matplotlib.dates.DateFormatter('%Y-%m-%d\n%H:%M:%S')


def plot(objs = objs_to_be_plotted, yscale='linear', maxy=4000):
    fig = plt.figure()
    all_graphs = []
    for n, i in enumerate(objs):
        i.ax = fig.add_subplot(1, 1, 1)
        i.ax.patch.set_facecolor('lightgrey')
        i.ax.xaxis.set_major_formatter(hfmt)
        plt.setp(i.ax.get_xticklabels(), size=8)
        i.ax.scatter(matplotlib.dates.date2num(i.dates), i.delays)
        i.ax.set_label(i.name)
        all_graphs.append(i.ax)
    plt.xlabel('Data e Hora', fontsize=24)
    plt.yscale(yscale)
    highestpoint = max([max(i.delays) for i in objs])
    if highestpoint < maxy:
        plt.ylim(0, maxy)
    else:
        count = 0
        if maxy > highestpoint:
            plt.ylim(0, highestpoint)
        else:
            plt.ylim(0, maxy)
            for o in objs:
                for d in o.delays:
                    if d > maxy:
                        count += 1
            print(f'{count} pontos fora do gráfico')

    plt.ylabel('Delay em segundos entre pacotes', fontsize=24)
    plt.legend([i.name for i in objs])
    plt.suptitle(f'Dados de delay para os ultimos {timefrom} dias')
    plt.grid()
    plt.show()

plot()
