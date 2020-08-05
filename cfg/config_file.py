from config_data_packet import Config_Data_Packet
from parameter import Parameter
import os

class Config_File:
    def __init__(self, filepath):
        self.data_packets = []
        with open(filepath, 'rb') as f:
            eof = f.seek(0, os.SEEK_END)
            f.seek(0)
            while f.tell() != eof:
                length = int.from_bytes(f.read(2), 'little')
                packet_id = int.from_bytes(f.read(1), 'little')
                param_count = int.from_bytes(f.read(2), 'little')
                params = f.read(length-5)
                p = Config_Data_Packet(length, packet_id, param_count, params)
                print(p)
                self.data_packets.append(p)

    def __repr__(self):
        param_count = 0
        for i in self.data_packets:
            param_count += i.param_count
        return f'[cfg file] <data packets:{len(self.data_packets)} params: {param_count}>'

if __name__ == '__main__':
    f = Config_File('config sample.fk4c')