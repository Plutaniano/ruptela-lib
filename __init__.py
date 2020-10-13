import logging

from .classes import Locator
from .devices import DeviceFactory
from .devices.fw import FW_File
from .devices.cfg import Config_File


logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
