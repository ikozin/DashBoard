from .bme280_base import Bme280_Base

class Bme280_Windows(Bme280_Base):
    """description of class"""

    def __init__(self, logger: Logger, address: int):
        """Initializes (declare internal variables)"""
        super(Bme280_Windows, self).__init__(logger)

    def read(self) -> (float, float, float):
        return (0, 0, 0)

