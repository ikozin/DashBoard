from halgpio import HalGpio
import subprocess


class HalGpio_OraPiWin(HalGpio):
    """description of class"""

    def init(self):
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
        subprocess.Popen("sudo reboot", shell=True)

    def shutdown(self):
        subprocess.Popen("sudo shutdown -h now", shell=True)

    def ledOn(self):
        pass

    def ledOff(self):
        pass
