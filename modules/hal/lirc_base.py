from abc import ABCMeta, abstractmethod
from logging import Logger


class Lirc_Base(metaclass=ABCMeta):
    """description of class"""

    def __init__(self, logger: Logger):
        """Initializes (declare internal variables)"""
        if not isinstance(logger, Logger):
            raise TypeError("Передаваемый параметр logger должен быть Logger")
        self._logger = logger

    def __del__(self):
        """Destructor"""
        pass

    @abstractmethod
    def getCode(self, code: str = None) -> str:
        pass
