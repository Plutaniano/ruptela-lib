import serial
import progressbar
import re
import requests
import os
from bs4 import BeautifulSoup

from .fw_data_packet import FW_Data_Packet

class FW_File:
    def __init__(self, path=None):
        if path == None:
            print('--->\t Buscando firmware mais recente.')
            fw_bytes = self._get_most_recent()
        else:
            fw_bytes = self._get_fw_from_file(path=path)
            print(f'--->\t Arquivo \"{path}\" encontrado.')

        self.data_packets = []
        for packet_id, i in enumerate(range(0, len(fw_bytes), 512)):
            chunk = fw_bytes[i:i+512]
            packet = FW_Data_Packet(chunk, packet_id + 1)
            self.data_packets.append(packet)
    
    def __repr__(self):
        return f'[FW_File] <data_packets:{len(self.data_packets)}>'

    def write(self, port, baud=115200, timeout=15):
        s = serial.Serial(port, baud, timeout=timeout)
        print('--->\t Iniciando comunicação com o dispositivo.')
        s.write(b'|FU_STRT*\r\n')

        expected = b'*FU_OK|\r\n'
        incoming = s.read(len(expected))
        if incoming != expected:
            raise ValueError(f'valor lido: {incoming}, esperado: {expected}')
        print('--->\t Atualização iniciada.')

        for p in progressbar.progressbar(self.data_packets):
            s.write(b'|FU_PCK*' + p.format() + b'\r\n')

            expected = b'*FU_OK|' + p.idf() + b'\r\n'
            incoming = s.read(len(expected))
            if incoming != expected:
                s.close()
                raise ValueError(f'valor lido: {incoming}, esperado: {expected}')
        
        print('--->\t Escrevendo firmware...')
        s.write(b'|FU_WRITE*\r\n')
        if s.read(9) != b'*FU_OK|\r\n':
            raise ValueError('Erro escrevendo firmware.')
        else:
            print('--->\t Sucesso.')
        s.write(b'|FU_END*')
        s.close()
        return 0
    
    @classmethod
    def _get_most_recent(cls):
        r = requests.get('https://doc.ruptela.lt/display/AB/FM-Eco4+S+Series')
        s = BeautifulSoup(r.content, features="html.parser")
        tag = s.find('a', text='FM-Eco4 S Series firmware & configurator')

        r = requests.get('https://doc.ruptela.lt' + tag['href'])
        s = BeautifulSoup(r.content, features="html.parser")
        regex = re.compile('FM.*efwk4')
        tag = s.find('a', text=regex)
        
        r = requests.get('https://doc.ruptela.lt' + tag['href'], allow_redirects=True)
        return r.content
    
    def _get_fw_from_file(cls, path=None):
        if path == None:
            for filename in os.listdir():
                if '.efwk4' in filename:
                    path = filename
                    break
            if path == None:
                raise FileNotFoundError('Arquivo de firmware (*.efwk4) não pode ser encontrado na pasta.')

        with open(path, 'rb') as f:
            file_bytes = f.read()
            return file_bytes
        
if __name__ == '__main__':
    f = FW_File(path='fw sample.efwk4')
