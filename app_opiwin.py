from app import Mainboard
from halgpio_opiwin import HalGpio_OraPiWin

FILE_SETTING = "setting_opiwin.ini"


if __name__ == "__main__":

    app = Mainboard(HalGpio_OraPiWin, FILE_SETTING)
    app.loop()
