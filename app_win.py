from app import Mainboard
from modules.hal.halgpio_windows import HalGpio_Windows
from modules.hal.bme280_windows import Bme280_Windows
from modules.hal.lirc_windows import Lirc_Windows

FILE_SETTING = "setting_win.ini"


if __name__ == "__main__":

    app = Mainboard(HalGpio_Windows, Bme280_Windows, Lirc_Windows, FILE_SETTING)
    app.loop()
