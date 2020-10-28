import logging

from .classes import Locator
from .devices import DeviceFactory
from .devices.fw import FW_File
from .devices.cfg import Config_File


logging.basicConfig(level=0, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
