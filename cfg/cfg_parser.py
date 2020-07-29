from cfgpacket import Data_Packet


with open('bytes','rb') as f:
    length = int.from_bytes(f.read(2), 'little')
    while length != 0:
        Data_Packet(length, f.read(length-2))
        length = int.from_bytes(f.read(2), 'little')
    

