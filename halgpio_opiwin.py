from typing import Callable
from halgpio import HalGpio
from logging import Logger
import subprocess
import OPi.GPIO as GPIO

# https://opi-gpio.readthedocs.io/en/latest/api-documentation.html

"""
'PL9' - 16
'PC4' - 18
'PD6' - 26
'PB4' - 29
'PB5' - 31
'PB6' - 33
'PB7' - 35
'PD5' - 37
"""

PIR_PIN = 'PD5' # 37
LED_PIN = 'PB7' # 35


class HalGpio_OraPiWin(HalGpio):
    """description of class"""

    def __init__(self, logger: Logger, func: Callable[[], None]):
        """Initializes (declare internal variables)"""
        super(HalGpio_OraPiWin, self).__init__(logger, func)
        self._counter = 0

    def init(self) -> None:
        GPIO.setmode(GPIO.SUNXI)
        GPIO.setup(LED_PIN, GPIO.OUT)
        GPIO.setup(PIR_PIN, GPIO.IN)
        self.ledOn()

    def done(self) -> None:
        GPIO.cleanup()

    def update(self) -> None:
        if self._counter > 100:
            self._counter = 0
            if GPIO.input(PIR_PIN) == GPIO.HIGH:
                self._func()
        self._counter += 1

    def display_off(self) -> None:
        subprocess.Popen("xset dpms force off > /dev/null 2>&1", shell=True).wait()

    def display_on(self) -> None:
        subprocess.Popen("xset dpms force on > /dev/null 2>&1", shell=True).wait()            

    def reboot(self) -> None:
        subprocess.Popen("sudo reboot", shell=True)

    def shutdown(self) -> None:
        subprocess.Popen("sudo shutdown -h now", shell=True)

    def ledOn(self) -> None:
        GPIO.output(LED_PIN, 1)

    def ledOff(self) -> None:
        GPIO.output(LED_PIN, 0)
