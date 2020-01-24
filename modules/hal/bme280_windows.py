from .bme280_base import Bme280_Base
from logging import Logger


class Bme280_Windows(Bme280_Base):
    """description of class"""

    def __init__(self, logger: Logger, address: int):
        """Initializes (declare internal variables)"""
        super(Bme280_Windows, self).__init__(logger)

    def read(self) -> (float, float, float):
        return (21.0, 1000.0, 40.0)
