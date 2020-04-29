from app import Mainboard
from modules.hal.halgpio_rasppi import HalGpio_RaspPi
from modules.hal.bme280_rasppi import Bme280_RaspPi
from modules.hal.lirc_rasppi import Lirc_RaspPi

FILE_SETTING = "setting_rasppi.ini"


if __name__ == "__main__":

    app = Mainboard(HalGpio_RaspPi, Bme280_RaspPi, Lirc_RaspPi, FILE_SETTING)
    app.loop()
