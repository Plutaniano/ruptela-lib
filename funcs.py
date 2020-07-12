import datetime
import requests
from classes import Object, Packet

URL = "https://api.fm-track.com/"

def create_all_objects():
    params = {
        "version": "1",
        "api_key": key,
    }

    r = requests.get(URL + 'objects', params=params)
    for i in r.json():
        Object(i)


def time_convert(time):
    if isinstance(time, str):
        return datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.000Z')
    else:
        return time.isoformat() + '.000Z'
