from typing import *

from serial.tools.list_ports import comports

from .web_user import Web_User
from .client import Client

class NotARuptelaDeviceError(BaseException):
    """
    Raised when trying to connected to a COM port that isn't connected
    to a Ruptela device.
    """
    def __init__(self, port) -> None:
        #Todo...
        pass

class AuthenticationError(BaseException):
    """
    Raised when an authentication attempt has failed.
    """
    def __init__(self, *args) -> None:
        super().__init__(f'Authentication failed. Credentials used: {args}.')

class PortNotFoundError(BaseException):
    """
    Raised when user-specified port, such as 'COM4', is not found.
    """
    def __init__(self, userinput) -> None:
        ports = [i.device for i in comports()]
        super().__init__(f'{userinput} not found in avaiable comports:{ports}')


class InvalidResponseError(BaseException):
    """
    Raised when unexpected response is received in serial communications.
    """
    def __init__(self, exp: bytes, recv: bytes) -> None:
        super().__init__(f'Expected: {exp}, received: {recv}')

class MissingAPIKeyError(BaseException):
    """
    Raised when API key not avaiable.
    """
    def __init__(self, obj: Union[Web_User, Client]) -> None:
        if hasattr(obj, 'web_users'):
            super().__init__(f'The client \'{obj}\' does not have a web user with an API key.')
        else:
            super().__init__(f'The web user \'{obj}\' from client \'{obj.client}\' does not have an API key.')
        
