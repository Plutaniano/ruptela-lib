import sqlite3 as sql
from classes import *
import datetime

create_all_objects()

conn = sql.connect('db/ruptela.db')
c = conn.cursor()

with open('db/lastupdate.txt', 'r') as f:
    timestamp = float(f.readlines()[0])
    delta = datetime.datetime.utcnow() - datetime.datetime.fromtimestamp(timestamp)
    timefrom = delta.days + delta.seconds / (60 * 60 * 24)
    timeto = time_convert(datetime.datetime.utcnow())
    print(f'timefrom: {timefrom}')

for o in Object.all:
    print(f'\n{o}', end='')
    for n, i in enumerate(o.get_interval(timefrom, timeto)):
        timestamp = time_convert(i['datetime']).timestamp()
        ignition_status = i['ignition_status']
        longitude = i['position']['longitude']
        latitude = i['position']['latitude']
        gps_odometer = i['inputs']['other']['virtual_gps_odometer']
        try:
            gsm_strength = i['inputs']['device_inputs']['gsm_signal_strength']
        except:
            gsm_strength = None
        params = (timestamp, ignition_status, latitude, longitude, gsm_strength, gps_odometer)
        c.execute(f'''INSERT INTO packets{o.imei} VALUES (?,?,?,?,?,?)''', params)
        print(f'\r{o} * {n}', end='')
    conn.commit()

open('db/lastupdate.txt', 'w').close()
with open('db/lastupdate.txt', 'w') as f:
    time = dt.datetime.utcnow().timestamp()
    f.write(str(time))
