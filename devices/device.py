from typing import *
from packaging import version
import time
import re
import logging

import progressbar
import serial
from serial.tools.list_ports import comports

from .cfg import Config_File
from .fw import FW_File
from ..classes.errors import *

import logging
logger = logging.getLogger(__name__)

class Device:
    """
    Base class for Ruptela devices.
    """
    firmwares = {}
    children = set()
    
    def __init__(self, comport, bootloader, fw_version, hardware, imei):
        if type(self) not in Device.children:
            Device.children.add(self)

        self.ser = serial.Serial(comport, 115200, timeout=30)
        self.ser.close()
        self.bootloader = bootloader
        self.fw_version = version.parse(fw_version)
        self.hardware = hardware
        self.imei = imei
        self._fw_file = ''
        self.status = 'Dispositivo conectado.'
        self.set_config()


    @property
    def fw_file(self) -> FW_File:
        """
        Property that will return the most recent firmware file avaiable.
        First it will check if the firmware has been already downloaded and
        saved in Device.firmwares. If it's already in Device.firmwares, it will
        return it, otherwise, it will download it, save it in Device.firmwares and
        then return it.
        """
        if self._fw_file == '':
            try:
                self._fw_file = Device.firmwares[self.device]
            except KeyError:
                Device.firmwares[self.device] = FW_File(self.device)
                self._fw_file = Device.firmwares[self.device]
        return self._fw_file

    def update(self) -> None:
        """
        Method for updating the device. Will check if the firmware currently
        in the device is more recent or equal to the most recent firmware avaiable
        before actually writing anything to the device.
        """
        if self.fw_version < self.fw_file.version:
            self._write_fw()
            return
        else:
            self.fwstatus = 'O dispositivo já está na última versão disponível.'
            logger.info('O dispositivo já está na última versão disponível.')
            return

    def _write_fw(self) -> None:
        """
        Method for writing the firmware bytes to the device. Performs no checks.
        If you want to update your device, use .update() instead.
        """
        with self.ser:
            self.ser.write(b'|FU_STRT*\r\n')
            expected = b'*FU_OK|\r\n'
            incoming = self.ser.readline()
            if incoming != expected:
                raise ValueError(f'valor lido: {incoming}, esperado: {expected}')
            logger.info('Atualização iniciada.')
            
            self.fwstatus = 0
            for p in progressbar.progressbar(self.fw_file.data_packets):
                self.fwstatus += 100//len(self.fw_file.data_packets)
                self.ser.write(b'|FU_PCK*' + p.format() + b'\r\n')
                expected = b'*FU_OK|' + p.idf() + b'\r\n'
                incoming = self.ser.read(len(expected))
                if incoming != expected:
                    raise ValueError(f'valor lido: {incoming}, esperado: {expected}')


            logger.info('Escrevendo firmware...')
            self.ser.write(b'|FU_WRITE*\r\n')
            expected = b'*FU_OK|\r\n'
            incoming = self.ser.read(len(expected))

            if incoming != expected:
                raise ValueError('Erro escrevendo firmware. Esperado: {expected}, recebido: {incoming}')
            else:
                self.fwstatus = 'Firmware gravado com sucesso.'
                logger.info('Aguardando reset.')
                time.sleep(18)
                logger.info('Sucesso.')
            self.ser.write(b'|FU_END*')
            return 
    
    def set_config(self, file: str = '') -> None:
        if isinstance(file, Config_File):
            self.config_file = file
            return

        if file == '':
            self.config_file = Config_File(self.config_ext)
        else:
            self.config_file = Config_File(file)

    def send_config(self, cfg: Config_File = '') -> None:
        """
        Method for sending a Config_File to the device. No checks before
        starting to write bytes to the device.
        """
        if cfg != '':
            self._write_config(cfg)
        else:
            self._write_config(self.config_file)

    def _write_config(self, cfg: Config_File) -> bool:
        """
        Method for writing the Config_File's bytes to the device. Performs no checks.
        If you want to update your config, use .send_config() instead.
        """
        with self.ser:
            logger.info('Iniciando comunicação com o dispositivo.')
            self.ser.write(b'#cfg_reset@\r\n')
            time.sleep(0.1)
            self.ser.write(b'#cfg_start@\r\n')
            time.sleep(0.1)

            expected_msg = b'@cfg_sts#10\r\n'
            msg_received = self.ser.read(len(expected_msg))
            if msg_received != expected_msg and msg_received != b'@cfg_sts#01\r\n':
                raise ValueError(f'valor lido: {msg_received}, esperado {expected_msg}')

            logger.info('Upload inicializado.')
            self.cfgstatus = 0
            for p in progressbar.progressbar(cfg.data_packets):
                self.cfgstatus += 100//len(cfg.data_packets)
                self.ser.write(b'#cfg_send@' + p.format() + b'*\r\n')

                expected_msg = b'@cfg_sts#1' + p.idf() + b'\r\n'
                msg_received = self.ser.read(len(expected_msg))
                if msg_received != expected_msg:
                    logger.error(f'Erro enviando data_packet. recebido:{msg_received}, esperado: {expected_msg}')
                    raise ValueError(f'Erro enviando data_packet. recebido:{msg_received}, esperado: {expected_msg}')
            
            logger.info('Escrevendo config.')
            self.cfgstatus = 'Escrevendo config.'
            self.ser.write(b'#cfg_write@\r\n')

            expected_msg = b'@cfg_sts#10'
            msg_received = self.ser.read(len(expected_msg))
            if msg_received != expected_msg:
                logger.error(f'Erro escrevendo config. msg: {msg_received}.')
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
                    logger.info('Sucesso.')
                    time.sleep(1)


    def is_connected(self):
        if self.ser.port in [i.device for i in comports()]:
            return True
        return False


class Eco4S(Device):
    """
    Class for the FM-Eco4 light+ S
    """
    device = 'Eco4S'
    config_ext = 'fk4c'
    template_id = '2531'
    hardwarelist = {
        'id': '157',
        'name': 'FM-Eco4 S',
        'description': 'FM-Eco4 S',
        'hw_version': 'FM-Eco4 S',
        'soft_id': '356',
        'soft_version': 'FM-Eco4 S'
    }

    def __init__(self, comport, bootloader, fw_version, hardware, imei) -> None:
        super().__init__(comport, bootloader, fw_version, hardware, imei)

Device.children.add(Eco4S)


class Eco4light(Device):
    """
    Class for the FM-Eco4 light+ S
    """

    device = 'Eco4light'
    config_ext = 'fe4c'
    template_id = '2553'
    hardwarelist = {
        'id': '138',
        'name': 'FM-Eco4 light',
        'description': 'FM-Eco4 light',
        'hw_version': 'FM-Eco4 light',
        'soft_id': '315',
        'soft_version': 'FM-Eco4 light'
    }
    def __init__(self, comport, bootloader, fw_version, hardware, imei) -> None:
        super().__init__(comport, bootloader, fw_version, hardware, imei)

Device.children.add(Eco4light)
    



def DeviceFactory(comport='') -> Union[Eco4light, Eco4S]:
    """
    Function for creating devices. Will automatically define which device
    to create based on response from said device to b"?version\\r\\n" sent on
    the serial port.
    """
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
                
                # b'?version\r\n'
                ser.write(b'?version\r\n')
                r = ser.read(100).decode('utf-8')
                bootloader = re.findall('0x[0-9a-fA-F]{2}', r)
                fw_version = re.findall('[\d\d\.]{11}', r)[0]
                hardware = re.findall('\w+-\w+-\w+', r)[0]

                # b'?imei\r\n'
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
