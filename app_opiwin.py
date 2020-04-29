from app import Mainboard
from modules.hal.halgpio_opiwin import HalGpio_OraPiWin
from modules.hal.bme280_opiwin import Bme280_OraPiWin
from modules.hal.lirc_opiwin import Lirc_OraPiWin

FILE_SETTING = "setting_opiwin.ini"


if __name__ == "__main__":

    app = Mainboard(HalGpio_OraPiWin, Bme280_OraPiWin, Lirc_OraPiWin, FILE_SETTING)
    app.loop()
