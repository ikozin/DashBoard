from halgpio import HalGpio
import subprocess
import RPi.GPIO as GPIO

PIR_PIN = 22  # GPIO22
LED_PIN = 23  # GPIO23


class HalGpio_RaspPi(HalGpio):
    """description of class"""

    def init(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(LED_PIN, GPIO.OUT)
        GPIO.setup(PIR_PIN, GPIO.IN)
        self.ledOn()
        GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=motion_detected)

    def done(self):
        GPIO.cleanup()

    def update(self):
        pass

    def display_off(self):
        # https://news.screenly.io/how-to-automatically-turn-off-and-on-your-monitor-from-your-raspberry-pi-5f259f40cae5,
        # https://elinux.org/RPI_vcgencmd_usage
        subprocess.Popen("vcgencmd display_power 0 > /dev/null 2>&1", shell=True).wait()

    def display_on(self):
        # https://news.screenly.io/how-to-automatically-turn-off-and-on-your-monitor-from-your-raspberry-pi-5f259f40cae5,
        # https://elinux.org/RPI_vcgencmd_usage
        subprocess.Popen("vcgencmd display_power 1 > /dev/null 2>&1", shell=True).wait()

    def reboot(self):
        subprocess.Popen("sudo reboot", shell=True)

    def shutdown(self):
        subprocess.Popen("sudo shutdown -h now", shell=True)

    def ledOn(self):
        GPIO.output(LED_PIN, 1)

    def ledOff(self):
        GPIO.output(LED_PIN, 0)

    def motion_detected(pin):
        # logger.debug("Motion detected!")
        #app.display_on()
        pass
