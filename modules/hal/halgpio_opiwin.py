import subprocess
import OPi.GPIO as GPIO

from .halgpio import HalGpio
from typing import Callable
from logging import Logger
from time import time


"""
# https://opi-gpio.readthedocs.io/en/latest/api-documentation.html
Orange Pi Win Plus
            ----------- ---------- ---- ---- ---------- -----------
PIR VCC -> |       3V3 |          |  1 | 2  |          | 5V        |
           |  TWI1-SDA |    [PH3] |  3 | 4  |          | 5V        |
           |  TWI1-SCK |    [PH2] |  5 | 6  |          | GND       |
           |     S_PWM |   [PL10] |  7 | 8  | [PL2]    | S_UART_TX |
           |       GND |          |  9 | 10 | [PL3]    | S_UART_RX |
           |  UART3_RX |    [PH5] | 11 | 12 | [PD4]    |           |
           |  UART3_TX |    [PH4] | 13 | 14 |          | GND       |
           | UART3_CTS |    [PH7] | 15 | 16 | [PL9]    |           |
           |       3V3 |          | 17 | 18 | [PC4]    |           |
           | SPI1_MOSI |    [PD2] | 19 | 20 |          | GND       |
           | SPI1_MISO |    [PD3] | 21 | 22 | [PH6]    | UART3_RTS |
           |  SPI1_CLK |    [PD1] | 23 | 24 | [PD0]    | SPI1_CS0  |
           |       GND |          | 25 | 26 | [PD6]    |           |
           |  TWI2-SDA |   [PE15] | 27 | 28 | [PE14]   | TWI2-SCK  |
           |           |    [PB4] | 29 | 30 |          | GND       |
           |           |    [PB5] | 31 | 32 | [PB2]    | UART2_RTS |
           |           |    [PB6] | 33 | 34 |          | GND       |
           |           |    [PB7] | 35 | 36 | [PB3]    | UART2_CTS |
PIR DATA-> |           |    [PD5] | 37 | 38 | [PB0]    | UART2_TX  |
PIR GND -> |       GND |          | 39 | 40 | [PB1]    | UART2_RX  |
            ----------- ---------- ---- ---- ---------- -----------

add_event_detect - ругается, нет прав
"""

PIR_PIN = 'PC4'  # PC4 - 18
LED_PIN = 'PL9'  # PL9 - 16


class HalGpio_OraPiWin(HalGpio):
    """description of class"""

    def __init__(self, logger: Logger, func: Callable[[], None]):
        """Initializes (declare internal variables)"""
        super(HalGpio_OraPiWin, self).__init__(logger, func)
        self._time = time()

    def init(self) -> None:
        GPIO.setmode(GPIO.SUNXI)
        GPIO.setup(LED_PIN, GPIO.OUT)
        GPIO.setup(PIR_PIN, GPIO.IN)
        self.ledOn()

    def done(self) -> None:
        GPIO.cleanup()

    def update(self) -> None:
        if time() - self._time > 1:
            self._time = time()
            if GPIO.input(PIR_PIN) == GPIO.HIGH:
                self._func()

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
