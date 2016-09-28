import configparser

from tkinter import *
from tkinter import ttk

from ext.ModalDialog import SelectFrame

class SwapManager(ttk.LabelFrame):
    """description of class"""

    def __init__(self, root):
        """ """
        super(SwapManager, self).__init__(root, text="Настройки модуля переключения")
        
        self._updateValue = IntVar()

        ttk.Label(self, text="Время обновления").grid(row=0, column=0, padx=2, pady=2)
        Spinbox(self, from_=5, to=60, increment=1, width=3, textvariable=self._updateValue).grid(row=0, column=1, padx=2, pady=2)
        ttk.Label(self, text="секунд").grid(row=0, column=2, padx=2, pady=2)
        self._frame = SelectFrame(self, "Выбор модулей")
        self._frame.grid(row=1, column=0, columnspan=3, sticky=(N,S,E,W), padx=2, pady=2)


    def load(self, config, modulelist):
        if not isinstance(config, configparser.ConfigParser): raise TypeError("config")
        if not config.has_section("SwapBlock"):      config.add_section("SwapBlock")
        section = config["SwapBlock"]
        self._updateValue.set(section.getint("UpdateTime", 10))
        selection = section.get("BlockList", "")
        selection = [item.strip(" '") for item in selection.split(",") if item.strip() in modulelist]
        self._frame.load(selection, modulelist)


    def save(self, config):
        """ """
        if not isinstance(config, configparser.ConfigParser): raise TypeError("config")
        if not config.has_section("SwapBlock"):      config.add_section("SwapBlock")
        section = config["SwapBlock"]
        section["UpdateTime"] = str(self._updateValue.get())
        section["BlockList"] = self._frame.getResult()
