# https://pypi.org/project/RPi.bme280/

import smbus2
import bme280

from .bme280_base import Bme280_Base
from logging import Logger


class Bme280_RaspPi(Bme280_Base):
    """description of class"""

    def __init__(self, logger: Logger, address: int):
        """Initializes (declare internal variables)"""
        super(Bme280_RaspPi, self).__init__(logger)
        self._port = 1
        self._address = address
        self._bus = smbus2.SMBus(self._port)
        self._calibration_params = bme280.load_calibration_params(self._bus, self._address)

    def read(self) -> (float, float, float):
        data = bme280.sample(self._bus, self._address, self._calibration_params)
        return (data.temperature, data.pressure, data.humidity)
