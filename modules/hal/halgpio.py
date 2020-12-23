from typing import Callable
from abc import ABCMeta, abstractmethod
from logging import Logger


class HalGpio(metaclass=ABCMeta):
    """description of class"""

    def __init__(self, logger: Logger, func: Callable[[], None], pir: int, led: int):
        """Initializes (declare internal variables)"""
        if not isinstance(logger, Logger):
            raise TypeError("Передаваемый параметр logger должен быть Logger")
        self._logger = logger
        self._func = func
        self._pir = pir
        self._led = led

    def __del__(self):
        """Destructor"""

    @abstractmethod
    def init(self) -> None:
        pass

    @abstractmethod
    def done(self) -> None:
        pass

    @abstractmethod
    def update(self) -> None:
        pass

    @abstractmethod
    def display_off(self) -> None:
        pass

    @abstractmethod
    def display_on(self) -> None:
        pass

    @abstractmethod
    def reboot(self) -> None:
        pass

    @abstractmethod
    def shutdown(self) -> None:
        pass

    @abstractmethod
    def ledOn(self) -> None:
        pass

    @abstractmethod
    def ledOff(self) -> None:
        pass
