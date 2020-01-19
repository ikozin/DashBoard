from .halgpio import HalGpio
from typing import Callable
from logging import Logger


class HalGpio_Windows(HalGpio):
    """description of class"""

    def __init__(self, logger: Logger, func: Callable[[], None]):
        """Initializes (declare internal variables)"""
        super(HalGpio_Windows, self).__init__(logger, func)

    def init(self) -> None:
        self._func()
        pass

    def done(self) -> None:
        pass

    def update(self) -> None:
        pass

    def display_off(self) -> None:
        pass

    def display_on(self) -> None:
        pass

    def reboot(self) -> None:
        pass

    def shutdown(self) -> None:
        pass

    def ledOn(self) -> None:
        pass

    def ledOff(self) -> None:
        pass
