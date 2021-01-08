import subprocess
from gpiozero import *

from .halgpio import HalGpio
from typing import Callable
from logging import Logger


"""

Raspberry Pi Model 4B Rev 1.2
            ----------- ---------- ---- ---- ---------- -----------
           |       3V3 |          |  1 | 2  |          | 5V        |
           |  I2C1_SDA |  [GPIO2] |  3 | 4  |          | 5V        |
           |  I2C1_SCL |  [GPIO3] |  5 | 6  |          | GND       |
           |           |  [GPIO4] |  7 | 8  | [GPIO14] | UART0_TX  |
           |       GND |          |  9 | 10 | [GPIO15] | UART0_RX  |
           |           | [GPIO17] | 11 | 12 | [GPIO18] | PCM_CLK   |
           |           | [GPIO27] | 13 | 14 |          | GND       |
           |           | [GPIO22] | 15 | 16 | [GPIO23] |           |
           |       3V3 |          | 17 | 18 | [GPIO24] |           |
           | SPI0_MOSI | [GPIO10] | 19 | 20 |          | GND       |
           | SPI0_MISO |  [GPIO9] | 21 | 22 | [GPIO25] |           |
           | SPI0_SCLK | [GPIO11] | 23 | 24 | [GPIO8]  | SPI0_CS0  |
           |       GND |          | 25 | 26 | [GPIO7]  | SPI0_CS1  |
           |     ID_SD |  [GPIO0] | 27 | 28 | [GPIO1]  | ID_SC     |
           |           |  [GPIO5] | 29 | 30 |          | GND       |
           |           |  [GPIO6] | 31 | 32 | [GPIO12] |           |
           |           | [GPIO13] | 33 | 34 |          | GND       |
           |           | [GPIO19] | 35 | 36 | [GPIO16] |           |
           |           | [GPIO26] | 37 | 38 | [GPIO20] |           |
           |       GND |          | 39 | 40 | [GPIO21] |           |
            ----------- ---------- ---- ---- ---------- -----------


"""

# PIR_PIN = 24  # GPIO23 - 18
# LED_PIN = 23  # GPIO24 - 16


class HalGpio_RaspPi4(HalGpio):
    """description of class"""

    def __init__(self, logger: Logger, func: Callable[[], None], pir: int, led: int):
        """Initializes (declare internal variables)"""
        super(HalGpio_RaspPi4, self).__init__(logger, func, pir, led)

    def init(self) -> None:
        self.pir = MotionSensor(self._pir)
        self.pir.when_motion = motion_detected
        self.led = LED(self._led) 
        self.led.on()

    def done(self) -> None:
        pass

    def update(self) -> None:
        pass

    def display_off(self) -> None:
        # https://news.screenly.io/how-to-automatically-turn-off-and-on-your-monitor-from-your-raspberry-pi-5f259f40cae5,
        # https://elinux.org/RPI_vcgencmd_usage
        subprocess.Popen("vcgencmd display_power 0 > /dev/null 2>&1", shell=True).wait()

    def display_on(self) -> None:
        # https://news.screenly.io/how-to-automatically-turn-off-and-on-your-monitor-from-your-raspberry-pi-5f259f40cae5,
        # https://elinux.org/RPI_vcgencmd_usage
        subprocess.Popen("vcgencmd display_power 1 > /dev/null 2>&1", shell=True).wait()

    def reboot(self) -> None:
        subprocess.Popen("sudo reboot", shell=True)

    def shutdown(self) -> None:
        subprocess.Popen("sudo shutdown -h now", shell=True)

    def ledOn(self) -> None:
        self.led.on()

    def ledOff(self) -> None:
        self.led.off()

    def motion_detected(self):
        # self._logger.debug("Motion detected!")
        self._func()
