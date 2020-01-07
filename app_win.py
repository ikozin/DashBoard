from app import Mainboard
from halgpio_windows import HalGpio_Windows

FILE_SETTING = "setting_win.ini"


if __name__ == "__main__":

    app = Mainboard(HalGpio_Windows, FILE_SETTING)
    app.loop()
