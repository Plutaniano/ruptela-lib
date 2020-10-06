from packaging import version

from typing import *
import time
import re

import serial
from ruptela.classes.errors import *
from serial.serialutil import SerialException
from serial.tools.list_ports import comports
from ruptela.devices.fw import FW_File


class Device:
    firmwares = {}
    
    def __init__(self, comport, bootloader, fw_version, hardware, imei):
        self.comport = comport
        self.ser = serial.Serial(comport, 115200, timeout=10)
        self.bootloader = bootloader
        self.fw_version = version.parse(fw_version)
        self.hardware = hardware
        self.imei = imei

    def update(self) -> bool:
        try:
            fw_file = Device.firmwares[self.device]
        except:
            Device.firmwares[self.device] = FW_File(device=self.device)
        
        fw_file = Device.firmwares[self.device]
        if self.fw_version < fw_file.version:
            fw_file.write(self.ser)
            return 0
        else:
            print('O dispositivo já na última versão disponível.')
            return 0
    
    def send_config(self, cfg) -> bool:
        try:
            cfg.write(self.ser)
            return 0
            
        except:
            print('Falha na gravação da config')
            return 1

    def is_alive(self):
        if self.ser.port in [i.device for i in comports()]:
            return True
        return False




class Eco4S(Device):
    """FM-Eco4 light+ S"""
    def __init__(self, comport, bootloader, fw_version, hardware, imei) -> None:
        super().__init__(comport, bootloader, fw_version, hardware, imei)
        self.device = 'Eco4S'


class Eco4light(Device):
    """FM-Eco4 light+ S"""
    def __init__(self, comport, bootloader, fw_version, hardware, imei) -> None:
        super().__init__(comport, bootloader, fw_version, hardware, imei)
        self.device = 'Eco4light'


def DeviceFactory(comport=''):
    com_ports = [i.device for i in comports()]

    if comport == '' and len(com_ports) == 1:
        comport = com_ports[0]

    if comport not in com_ports:
        raise PortNotFoundError
    else:
        port_info = comports()[com_ports.index(comport)]

    if 'STMicro' not in port_info.description:
        raise NotARuptelaDeviceError

    for i in range(3):
        bootloader = ''
        fw_version = ''
        hardware = ''
        imei = ''

        try:
            with serial.Serial(port_info.device, 115200, timeout=1) as ser:
                ser.write(b'?version\r\n')
                r = ser.read(100).decode('utf-8')
                bootloader = re.findall('0x[0-9a-fA-F]{2}', r)
                fw_version = re.findall('[\d\d\.]{11}', r)[0]
                hardware = re.findall('\w+-\w+-\w+', r)[0]

                ser.write(b'?imei\r\n')
                r = ser.readline().decode('utf-8')
                imei = re.findall('[0-9]+', r)[0]
                
        except Exception as e:
            print(f'{i}\r')
            time.sleep(3)
            raise SerialException

    assert (bootloader and fw_version and hardware and imei)
    
    if 'FMEGL4' in hardware:
        return Eco4light(comport, bootloader, fw_version, hardware, imei)
    
    if 'FMES4' in hardware:
        return Eco4S(comport, bootloader, fw_version, hardware, imei)
