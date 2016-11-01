import configparser

from tkinter import *
from tkinter import font
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import colorchooser

from ext.BaseManager import BaseManager
from ext.ModalDialog import FontChooserFrame
from ext.ModalDialog import XYFrame


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

        self._posCO2 = XYFrame(self, "Расположение для CO2", "Расположение (X)", "Расположение (Y)")
        self._posCO2.grid(row=2, column=0, columnspan=2, padx=2, pady=2, sticky=(N,S,E,W))
        self._posTemp = XYFrame(self, "Расположение для Температуры", "Расположение (X)", "Расположение (Y)")
        self._posTemp.grid(row=3, column=0, columnspan=2, padx=2, pady=2, sticky=(N,S,E,W))

        self._co2 = FontChooserFrame(self, "Параметры шрифта CO2")
        self._co2.grid(row=4, column=0, columnspan=2, padx=2, pady=2, sticky=(N,S,E,W))
        self._temp = FontChooserFrame(self, "Параметры шрифта Температуры")
        self._temp.grid(row=5, column=0, columnspan=2, padx=2, pady=2, sticky=(N,S,E,W))


    def load(self, config, modulelist):
        if not isinstance(config, configparser.ConfigParser): raise TypeError("config")
        if not config.has_section("MT8057Block"):      config.add_section("MT8057Block")
        section = config["MT8057Block"]
        self._maxGreenValue.set(section.getint("Green", 600))
        self._maxYellowValue.set(section.getint("Yellow", 800))

        fontName = section.get("CO2FontName", "Helvetica")
        fontSize = section.getint("CO2FontSize", 64)
        isBold = section.getboolean("CO2FontBold", True)
        isItalic = section.getboolean("CO2FontItalic", False)
        self._co2.load(fontName, fontSize, isBold, isItalic)

        fontName = section.get("TempFontName", "Helvetica")
        fontSize = section.getint("TempFontSize", 64)
        isBold = section.getboolean("TempFontBold", True)
        isItalic = section.getboolean("TempFontItalic", False)
        self._temp.load(fontName, fontSize, isBold, isItalic)

        (posX, posY) = self._getTuple(section.get("CO2Pos", "(0, 0)"))
        self._posCO2.load(posX, posY)
        (posX, posY) = self._getTuple(section.get("TempPos", "(0, 0)"))
        self._posTemp.load(posX, posY)


    def save(self, config):
        if not isinstance(config, configparser.ConfigParser): raise TypeError("config")
        if not config.has_section("MT8057Block"):      config.add_section("MT8057Block")
        section = config["MT8057Block"]
        section["Green"] = str(self._maxGreenValue.get())
        section["Yellow"] = str(self._maxYellowValue.get())

        (fontName, fontSize, isBold, isItalic) = self._co2.getResult()
        section["CO2FontName"]   = fontName
        section["CO2FontSize"]   = str(fontSize)
        section["CO2FontBold"]   = str(isBold)
        section["CO2FontItalic"] = str(isItalic)

        (fontName, fontSize, isBold, isItalic) = self._temp.getResult()
        section["TempFontName"]   = fontName
        section["TempFontSize"]   = str(fontSize)
        section["TempFontBold"]   = str(isBold)
        section["TempFontItalic"] = str(isItalic)

        (posX, posY) = self._posCO2.getResult()
        section["CO2Pos"] = "({0},{1})".format(posX, posY)
        (posX, posY) = self._posTemp.getResult()
        section["TempPos"] = "({0},{1})".format(posX, posY)


    def _getTuple(self, value):
        """  Конвертирует строку '0, 0, 0' в кортеж (0, 0, 0) """
        try:
            return tuple(int(item.strip("([ '])")) for item in value.split(",") if item.strip())
        except Exception as ex:
            return None
