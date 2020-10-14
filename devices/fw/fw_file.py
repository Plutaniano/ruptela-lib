import serial
import progressbar
import re
from packaging import version as vers
import requests
import os
from bs4 import BeautifulSoup

from .fw_data_packet import FW_Data_Packet

import logging
logger = logging.getLogger(__name__)

class FW_File:
    def __init__(self, device: str = 'Eco4S', path: str = None) -> None:
        self.progress = 'stopped'
        self.device = device
        if path == None:
            logger.info('Buscando firmware mais recente.')
            fw_bytes = self._get_most_recent()
        else:
            fw_bytes = self._get_fw_from_file(path=path)
            logger.info(f'Arquivo \"{path}\" encontrado.')

        self.data_packets = []
        for packet_id, i in enumerate(range(0, len(fw_bytes), 512)):
            chunk = fw_bytes[i:i+512]
            packet = FW_Data_Packet(chunk, packet_id + 1)
            self.data_packets.append(packet)
    
    def _get_most_recent(self) -> bytes:
        links = {
            'Eco4S': ('https://doc.ruptela.lt/display/AB/FM-Eco4+S+Series', 'FM-Eco4 S Series firmware & configurator'),
            'Eco4light': ('https://doc.ruptela.lt/pages/viewpage.action?pageId=884810', 'FM-Eco4 light/light+/3G firmwares & configurators')
        }
        r = requests.get(links[self.device][0])
        s = BeautifulSoup(r.content, features="html.parser")
        tag = s.find('a', text=links[self.device][1])

        r = requests.get('https://doc.ruptela.lt' + tag['href'])
        s = BeautifulSoup(r.content, features="html.parser")
        regex = re.compile('FM.*\..*4')
        tag = s.find('a', text=regex)
        self.version = vers.parse(tag.text[-17:-6])
        logger.info(f'Arquivo: {tag.text}')
        
        r = requests.get('https://doc.ruptela.lt' + tag['href'], allow_redirects=True)
        return r.content
    
    def _get_fw_from_file(self, path: str = '') -> bytes:
        """
        
        """
        if path == '':
            for filename in os.listdir():
                if '.efwk4' in filename:
                    path = filename
                    break
                raise FileNotFoundError('Arquivo de firmware (*.efwk4) não pode ser encontrado na pasta.')

        with open(path, 'rb') as f:
            file_bytes = f.read()
            return file_bytes

    def __repr__(self) -> str:
        return f'[FW_File] <version: {self.version}, data_packets:{len(self.data_packets)}>'
        
if __name__ == '__main__':
    f = FW_File(path='fw sample.efwk4')
