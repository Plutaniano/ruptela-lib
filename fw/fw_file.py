import serial
import progressbar
from fw_data_packet import FW_Data_Packet

class FW_File:
    def __init__(self, path):
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
        print('[ * ] Iniciando atualização de firmware.')
        s.write(b'|FU_STRT*\r\n')

        incoming = s.read(9)
        if incoming != b'*FU_OK|\r\n':
            raise ValueError(f'valor lido: {incoming}')
        print('--- Atualização iniciada.')

        for p in progressbar.progressbar(self.data_packets):
            s.write(b'|FU_PCK*' + p.format() + b'*\r\n')
            incoming = s.read(11)
            if incoming != b'*FU_OK|' + p.idf() + b'\r\n':
                raise ValueError(f'valor lido: {incoming}')
        
        print('-- escrevendo fw...')
        s.write(b'|FU_WRITE*\r\n')
        if s.read(9) != b'*FU_OK|\r\n':
            print('[ERR] erro escrevendo fw.')
        else:
            print('[OK ] sucesso')
        s.close()


if __name__ == '__main__':
    f = FW_File('fw sample.efwk4')
