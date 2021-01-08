from app import Mainboard
from modules.hal.halgpio_rasppi4 import HalGpio_RaspPi4
from modules.hal.bme280_rasppi import Bme280_RaspPi
from modules.hal.lirc_rasppi import Lirc_RaspPi

FILE_SETTING = "setting_rasppi4.ini"


if __name__ == "__main__":

    app = Mainboard(HalGpio_RaspPi4, Bme280_RaspPi, Lirc_RaspPi, FILE_SETTING)
    app.loop()
