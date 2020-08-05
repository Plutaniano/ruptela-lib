from config_data_packet import Config_Data_Packet
from parameter import Parameter
import os

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

    def write(self):
        s = serial.Serial(port, baud, timeout=timeout)
        print('[ * ] Iniciando upload de configuração.')
        s.write(b'#cfg_start@\r\n')

        incoming = s.read(9)
        if incoming != b'@cfg_sts#10\r\n':
            raise ValueError(f'valor lido: {incoming}')

        print('--- Upload inicializado.')
        for p in progressbar.progressbar(self.data_packets):
            s.write(b'#cfg_send@' + p.format() + b'*\r\n')
            incoming = s.read(11)
            if incoming != b'*FU_OK|' + p.idf() + b'\r\n':
                raise ValueError(f'valor lido: {incoming}')
        
        print('--- escrevendo config.')
        s.write(b'|FU_WRITE*\r\n')
        if s.read(9) != b'*FU_OK|\r\n':
            print('[ERR] erro escrevendo config.')
        else:
            print('[ * ] sucesso')
        s.close()

if __name__ == '__main__':
    f = Config_File('config sample.fk4c')