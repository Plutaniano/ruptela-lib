from config_data_packet import Config_Data_Packet
from parameter import Parameter

class Config_File:
    def __init__(self, filepath):
        self.data_packets = []
        with open(filepath, 'rb') as f:
            length = int.from_bytes(f.read(2), 'little')
            while length != 0:
                p = Config_Data_Packet(length, f.read(length-2))
                self.data_packets.append(p)
                length = int.from_bytes(f.read(2), 'little')

    def __repr__(self):
        param_count = 0
        for i in self.data_packets:
            param_count += i.param_count
        return f'[cfg file] <data packets:{len(self.data_packets)} params: {param_count}>'

if __name__ == '__main__':
    f = Config_File('config sample.fk4c')