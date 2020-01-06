from typing import Callable
from halgpio import HalGpio


class HalGpio_Windows(HalGpio):
    """description of class"""

    def __init__(self, logger, func: Callable[[], None]):
        """Initializes (declare internal variables)"""
        super(HalGpio_Windows, self).__init__(logger, func)

    def init(self):
        self._func()
        pass

    def done(self):
        pass

    def update(self):
        pass

    def display_off(self):
        pass

    def display_on(self):
        pass

    def reboot(self):
        pass

    def shutdown(self):
        pass

    def ledOn(self):
        pass

    def ledOff(self):
        pass
