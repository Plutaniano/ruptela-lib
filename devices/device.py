from packaging import version
import progressbar

from typing import *
import time
import re

import serial
from .cfg import Config_File
from ruptela.classes.errors import *
from serial.serialutil import SerialException
from serial.tools.list_ports import comports
from ruptela.devices.fw import FW_File


class Device:
    firmwares = {}
    
    def __init__(self, comport, bootloader, fw_version, hardware, imei):
        self.ser = serial.Serial(comport, 115200, timeout=15)
        self.ser.close()
        self.bootloader = bootloader
        self.fw_version = version.parse(fw_version)
        self.hardware = hardware
        self.imei = imei
        self._fw_file = ''
        self.status = 'Dispositivo conectado.'


    @property
    def fw_file(self):
        if self._fw_file == '':
            try:
                self._fw_file = Device.firmwares[self.device]
            except KeyError:
                Device.firmwares[self.device] = FW_File(self.device)
                self._fw_file = Device.firmwares[self.device]
                return self._fw_file
        else:
            return self._fw_file

    def update(self) -> bool:
        if self.fw_version < self.fw_file.version:
            return self._write_fw()
        else:
            self.fwstatus = 'O dispositivo já está na última versão disponível.'
            print('O dispositivo já está na última versão disponível.')
            return 0

    def _write_fw(self) -> bool:
        with self.ser:
            self.ser.write(b'|FU_STRT*\r\n')
            expected = b'*FU_OK|\r\n'
            incoming = self.ser.read(len(expected))
            if incoming != expected:
                raise ValueError(f'valor lido: {incoming}, esperado: {expected}')
            print('--->\t Atualização iniciada.')
            
            self.fwstatus = '0%'
            for p in progressbar.progressbar(self.fw_file.data_packets):
                self.fwstatus += 100//len(self.fw_file.data_packets)
                self.ser.write(b'|FU_PCK*' + p.format() + b'\r\n')
                expected = b'*FU_OK|' + p.idf() + b'\r\n'
                incoming = self.ser.read(len(expected))
                if incoming != expected:
                    raise ValueError(f'valor lido: {incoming}, esperado: {expected}')


            print('--->\t Escrevendo firmware...')
            self.ser.write(b'|FU_WRITE*\r\n')
            expected = b'*FU_OK|\r\n'
            incoming = self.ser.read(len(expected))

            if incoming != expected:
                raise ValueError('Erro escrevendo firmware. Esperado: {expected}, recebido: {incoming}')
            else:
                self.fwstatus = 'Firmware gravado com sucesso.'
                print('--->\t Sucesso.')
            self.ser.write(b'|FU_END*')
            return 0
    
    def send_config(self, cfg: Config_File) -> bool:
        return self._write_config(cfg)
    
    def _write_config(self, cfg: Config_File) -> bool:
        with self.ser:
            print('--->\t Iniciando comunicação com o dispositivo.')
            self.ser.write(b'#cfg_reset@\r\n')
            time.sleep(0.1)
            self.ser.write(b'#cfg_start@\r\n')
            time.sleep(0.1)

            expected_msg = b'@cfg_sts#10\r\n'
            msg_received = self.ser.read(len(expected_msg))
            if msg_received != expected_msg and msg_received != b'@cfg_sts#01\r\n':
                raise ValueError(f'valor lido: {msg_received}, esperado {expected_msg}')

            print('--->\t Upload inicializado.')
            self.cfgstatus = 0
            for p in progressbar.progressbar(cfg.data_packets):
                self.cfgstatus += 100//len(cfg.data_packets)
                self.ser.write(b'#cfg_send@' + p.format() + b'*\r\n')

                expected_msg = b'@cfg_sts#1' + p.idf() + b'\r\n'
                msg_received = self.ser.read(len(expected_msg))
                if msg_received != expected_msg:
                    raise ValueError(f'[ERR] erro enviando data_packet. recebido:{msg_received}, esperado: {expected_msg}')
            
            print('--->\t escrevendo config.')
            self.cfgstatus = 'Escrevendo config.'
            self.ser.write(b'#cfg_write@\r\n')

            expected_msg = b'@cfg_sts#10'
            msg_received = self.ser.read(len(expected_msg))
            if msg_received != expected_msg:
                raise ValueError(f'[ERR] erro escrevendo config. msg:{msg_received}')
            else:
                self.ser.write(b'#cfg_end@\r\n')

                expected_msg = b'\r\n@cfg_sts#\x31\x30\r\n'
                msg_received = self.ser.read(len(expected_msg))
                if msg_received != expected_msg:
                    raise ValueError(f'[ERR] erro na resposta do pedido de escrita. msg:{msg_received}')
                else:
                    self.cfgstatus = 'Config escrita com sucesso.'
                    del self.status
                    print('--->\t Sucesso.')
                    time.sleep(1)
            return 0

    def is_connected(self):
        if self.ser.port in [i.device for i in comports()]:
            return True
        return False


class Eco4S(Device):
    """FM-Eco4 light+ S"""
    def __init__(self, comport, bootloader, fw_version, hardware, imei) -> None:
        self.device = 'Eco4S'
        super().__init__(comport, bootloader, fw_version, hardware, imei)


class Eco4light(Device):
    """FM-Eco4 light+ S"""
    def __init__(self, comport, bootloader, fw_version, hardware, imei) -> None:
        self.device = 'Eco4light'
        super().__init__(comport, bootloader, fw_version, hardware, imei)


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
    
    bootloader = ''
    fw_version = ''
    hardware = ''
    imei = ''
    for i in range(3):
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
                
        except Exception:
            if i != 2:
                time.sleep(3)
    
    assert bootloader != ''
    assert fw_version != ''
    assert hardware != ''
    assert imei != ''
    
    if 'FMEGL4' in hardware:
        return Eco4light(comport, bootloader, fw_version, hardware, imei)
    
    if 'FMES4' in hardware:
        return Eco4S(comport, bootloader, fw_version, hardware, imei)
