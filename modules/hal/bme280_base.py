from abc import ABCMeta, abstractmethod
from logging import Logger


class Bme280_Base(metaclass=ABCMeta):
    """description of class"""

    def __init__(self, logger: Logger):
        """Initializes (declare internal variables)"""
        if not isinstance(logger, Logger):
            raise TypeError("Передаваемый параметр logger должен быть Logger")
        self._logger = logger

    def __del__(self):
        """Destructor"""

    @abstractmethod
    def read(self) -> (float, float, float):
        pass
