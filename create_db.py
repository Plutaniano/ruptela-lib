import sqlite3 as sql
from classes import *

create_all_objects()

conn = sql.connect('db/ruptela.db')
c = conn.cursor()

timefrom = float(input('timefrom? '))

c.execute('''CREATE TABLE objects (imei text, id text, name text)''')

open('db/lastupdate.txt', 'w').close()
with open('db/lastupdate.txt', 'w') as f:
    time = dt.datetime.utcnow()
    f.write(str(time.timestamp()))

for o in Object.all:
    print(f'{o}', end='')
    obj_params = (o.imei, o.id, o.name)
    c.execute('''INSERT INTO objects VALUES (?,?,?)''', obj_params)
    c.execute(f'''CREATE TABLE packets{o.imei} (timestamp timestamp, ignition_status text, latitude real, longitude real, gsm_signal_strength integer, virtual_gps_odometer float)''')
    timeto = (dt.datetime.utcnow() - time).total_seconds() / (60 * 60 * 24)
    for n, i in enumerate(o.get_interval(timefrom, timeto)):
        timestamp = time_convert(i['datetime']).timestamp()
        ignition_status = i['ignition_status']
        longitude = i['position']['longitude']
        latitude = i['position']['latitude']
        try:
            gps_odometer = i['inputs']['other']['virtual_gps_odometer']
        except:
            gps_odometer = None
        try:
            gsm_strength = i['inputs']['device_inputs']['gsm_signal_strength']
        except:
            gsm_strength = None
        params = (timestamp, ignition_status, latitude, longitude, gsm_strength, gps_odometer)
        c.execute(f'''INSERT INTO packets{o.imei} VALUES (?,?,?,?,?,?)''', params)
        print(f'\r{o} * {n}', end='')
    print('\n')
    conn.commit()
