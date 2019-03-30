from typing import *

from configparser import ConfigParser
from tkinter import *

from ext.BaseManager import BaseManager
from ext.ModalDialog import SelectFrame


class SwapManager(BaseManager):
    """description of class"""

    def __init__(self, root: LabelFrame):
        """ """
        super(SwapManager, self).__init__(root, text="Настройки модуля переключения")

        self._updateValue = IntVar()

        lbl = Label(self, text="Время обновления")
        lbl.grid(row=0, column=0, padx=2, pady=2)

        spin = Spinbox(self, from_=5, to=60, increment=1, width=3, textvariable=self._updateValue)
        spin.grid(row=0, column=1, padx=2, pady=2)

        lbl = Label(self, text="секунд")
        lbl.grid(row=0, column=2, padx=2, pady=2)

        self._frame = SelectFrame(self, "Выбор модулей")
        self._frame.grid(row=1, column=0, columnspan=3, sticky=(N, S, E, W), padx=2, pady=2)

    def load(self, config: ConfigParser, modulelist: Dict[str, BaseManager]) -> None:
        if not isinstance(config, ConfigParser):
            raise TypeError("config")
        if not config.has_section("SwapBlock"):
            config.add_section("SwapBlock")
        section = config["SwapBlock"]
        self._updateValue.set(section.getint("UpdateTime", 10))
        selection = section.get("BlockList", "")
        selection = [item.strip(" '") for item in selection.split(",") if item.strip() in modulelist]
        self._frame.load(selection, modulelist)

    def save(self, config: ConfigParser) -> None:
        """ """
        if not isinstance(config, ConfigParser):
            raise TypeError("config")
        if not config.has_section("SwapBlock"):
            config.add_section("SwapBlock")
        section = config["SwapBlock"]
        section["UpdateTime"] = str(self._updateValue.get())
        section["BlockList"] = self._frame.getResult()
