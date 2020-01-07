from typing import Callable
from .halgpio import HalGpio
from logging import Logger
import subprocess
import RPi.GPIO as GPIO

PIR_PIN = 22  # GPIO22
LED_PIN = 23  # GPIO23


class HalGpio_RaspPi(HalGpio):
    """description of class"""

    def __init__(self, logger: Logger, func: Callable[[], None]):
        """Initializes (declare internal variables)"""
        super(HalGpio_RaspPi, self).__init__(logger, func)

    def init(self) -> None:
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(LED_PIN, GPIO.OUT)
        GPIO.setup(PIR_PIN, GPIO.IN)
        self.ledOn()
        GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=self.motion_detected)

    def done(self) -> None:
        GPIO.cleanup()

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
        GPIO.output(LED_PIN, 1)

    def ledOff(self) -> None:
        GPIO.output(LED_PIN, 0)

    def motion_detected(self, pin):
        self._logger.debug("Motion detected!")
        self._func()
