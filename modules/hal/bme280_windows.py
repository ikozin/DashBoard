from .bme280_base import Bme280_Base
from logging import Logger


class Bme280_Windows(Bme280_Base):
    """description of class"""

    def __init__(self, logger: Logger, address: int):
        """Initializes (declare internal variables)"""
        super(Bme280_Windows, self).__init__(logger)
        self._temperature: float = 21.0
        self._pressure: float = 1000.0
        self._humidity: float = 40.0

    def read(self) -> (float, float, float):
        self._temperature += 1.0
        self._pressure += 1.0
        self._humidity += 1.0
        return (self._temperature, self._pressure, self._humidity)
