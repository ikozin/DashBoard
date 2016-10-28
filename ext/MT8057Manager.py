import configparser

from tkinter import *
from tkinter import font
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import colorchooser

from ext.BaseManager import BaseManager


class MT8057Manager(BaseManager):
    """description of class"""

    def __init__(self, root):
        """ """
        super(MT8057Manager, self).__init__(root, text="Настройки MT8057")
        self._maxGreenValue = IntVar()
        self._maxYellowValue = IntVar()
        ttk.Label(self, text="Максимум зеленой зоны").grid(row=0, column=0, padx=2, pady=2)
        ttk.Entry(self, textvariable=self._maxGreenValue, width=4).grid(row=0, column=1, padx=2, pady=2)
        ttk.Label(self, text="Максимум желтой зоны").grid(row=1, column=0, padx=2, pady=2)
        ttk.Entry(self, textvariable=self._maxYellowValue, width=4).grid(row=1, column=1, padx=2, pady=2)


    def load(self, config, modulelist):
        if not isinstance(config, configparser.ConfigParser): raise TypeError("config")
        if not config.has_section("MT8057Block"):      config.add_section("MT8057Block")
        section = config["MT8057Block"]
        self._maxGreenValue.set(section.getint("Green", 600))
        self._maxYellowValue.set(section.getint("Yellow", 800))


    def save(self, config):
        if not isinstance(config, configparser.ConfigParser): raise TypeError("config")
        if not config.has_section("MT8057Block"):      config.add_section("MT8057Block")
        section = config["MT8057Block"]
        section["Green"] = str(self._maxGreenValue.get())
        section["Yellow"] = str(self._maxYellowValue.get())
