from .config_data_packet import Config_Data_Packet
from .parameter import Parameter
import serial
import progressbar
import os
import time

class Config_File:
    def __init__(self, filepath=''):
        if filepath == '':
            for filename in os.listdir():
                if '.fk4c' in filename:
                    filepath = filename
                    break
        if filepath == '':
            raise FileNotFoundError('Arquivo de config (*.fk4c) não pode ser encontrado.')

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
                self.data_packets.append(p)

    def __repr__(self):
        param_count = 0
        for i in self.data_packets:
            param_count += i.param_count
        return f'[cfg file] <data packets:{len(self.data_packets)} params: {param_count}>'

    def write(self, port='', baud=115200, timeout=10):
        if isinstance(port, serial.Serial):
            s = port
        else:
            s = serial.Serial(port, baud, timeout=timeout)
            
        print('--->\t Iniciando comunicação com o dispositivo.')
        s.write(b'#cfg_reset@\r\n')
        time.sleep(0.01)
        s.write(b'#cfg_start@\r\n')

        expected_msg = b'@cfg_sts#10\r\n'
        msg_received = s.read(len(expected_msg))

        if msg_received != expected_msg and msg_received != b'@cfg_sts#01\r\n':
            raise ValueError(f'valor lido: {msg_received}, esperado {expected_msg}')

        print('--->\t Upload inicializado.')
        for p in progressbar.progressbar(self.data_packets):
            s.write(b'#cfg_send@' + p.format() + b'*\r\n')

            expected_msg = b'@cfg_sts#1' + p.idf() + b'\r\n'
            msg_received = s.read(len(expected_msg))
            if msg_received != expected_msg:
                raise ValueError(f'[ERR] erro enviando data_packet. recebido:{msg_received}, esperado: {expected_msg}')
        
        print('--->\t escrevendo config.')
        s.write(b'#cfg_write@\r\n')

        expected_msg = b'@cfg_sts#10'
        msg_received = s.read(len(expected_msg))
        if msg_received != expected_msg:
            raise ValueError(f'[ERR] erro escrevendo config. msg:{msg_received}')
        else:
            s.write(b'#cfg_end@\r\n')

            expected_msg = b'\r\n@cfg_sts#\x31\x30\r\n'
            msg_received = s.read(len(expected_msg))
            if msg_received != expected_msg:
                raise ValueError(f'[ERR] erro na resposta do pedido de escrita. msg:{msg_received}')
            else:
                print('--->\t Sucesso.')
                time.sleep(1)
        s.close()
        return 0

if __name__ == '__main__':
    f = Config_File('config sample.fk4c')