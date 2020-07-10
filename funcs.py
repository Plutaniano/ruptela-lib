import datetime
import requests
from classes import Object,Packet

KEY = "Al-xrBlaeH-JXIj0RuPQT6FwuPFrZZGd"
URL = "https://api.fm-track.com/"


def getAllObjects(key=KEY):
    params = {
        "version": "1",
        "api_key": key,
    }

    r = requests.get(URL + 'objects', params=params)
    return r.json()

def create_all_objects():
    for i in getAllObjects():
        Object(i)


def time_convert(time):
    if isinstance(time, str):
        return datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.000Z')
    else:
        return time.isoformat() + '.000Z'
