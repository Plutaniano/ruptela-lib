import serial
import progressbar
import os
from .fw_data_packet import FW_Data_Packet

class FW_File:
    def __init__(self, path=''):
        if path == '':
            for filename in os.listdir():
                if '.efwk4' in filename:
                    path = filename
                    break
        if path == '':
            raise FileNotFoundError('Arquivo de firmware (*.efwk4) não pode ser encontrado.')       

        print(f'--->\t Arquivo \"{path}\" encontrado.')
        with open(path, 'rb') as f:
            file_bytes = f.read()
            self.data_packets = []
            for packet_id, i in enumerate(range(0, len(file_bytes), 512)):
                chunk = file_bytes[i:i+512]
                packet = FW_Data_Packet(chunk, packet_id + 1)
                self.data_packets.append(packet)
    
    def __repr__(self):
        return f'[FW_File] <data_packets:{len(self.data_packets)}>'

    def write(self, port, baud=115200, timeout=10):
        s = serial.Serial(port, baud, timeout=timeout)
        print('--->\t Iniciando comunicação com o dispositivo.')
        s.write(b'|FU_STRT*\r\n')

        expected = b'*FU_OK|\r\n'
        incoming = s.read(len(expected))
        if incoming != expected:
            raise ValueError(f'valor lido: {incoming}, esperado: {expected}')
        print('--->\t Atualização iniciada.')

        for p in progressbar.progressbar(self.data_packets):
            s.write(b'|FU_PCK*' + p.format() + b'*\r\n')

            expected = b'*FU_OK|' + p.idf() + b'\r\n'
            incoming = s.read(len(expected))
            if incoming != expected:
                raise ValueError(f'valor lido: {incoming}, esperado: {expected}')
        
        print('--->\t Escrevendo firmware...')
        s.write(b'|FU_WRITE*\r\n')
        if s.read(9) != b'*FU_OK|\r\n':
            raise ValueError('Erro escrevendo firmware.')
        else:
            print('--->\t Sucesso.')
        s.close()
        return 0


if __name__ == '__main__':
    f = FW_File('fw sample.efwk4')
