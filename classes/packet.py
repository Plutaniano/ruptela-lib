import datetime

class Packet:
    def __init__(self, d, owner):
        self.object = owner
        self.object_id = d['object_id']
        self.datetime = datetime.datetime.strptime(d['datetime'], '%Y-%m-%dT%H:%M:%S.%fZ')
        self.ignition_status = d['ignition_status']
        self.position = d['position']
        self.virtual_gps_odometer = d['inputs']['other']['virtual_gps_odometer']
        try:
            self.gsm_signal_strength = d['inputs']['device_inputs']['gsm_signal_strength']
        except:
            self.gsm_signal_strength = None
        self.virtual_odometer = d['inputs']['device_inputs']['virtual_odometer']

    def __repr__(self):
        return f'[{self.object.name}][{self.datetime.isoformat()}] [gsm:{self.gsm_signal_strength}]'