from app import Mainboard
from modules.hal.halgpio_rasppi import HalGpio_RaspPi

FILE_SETTING = "setting_rasppi.ini"


if __name__ == "__main__":

    app = Mainboard(HalGpio_RaspPi, FILE_SETTING)
    app.loop()
