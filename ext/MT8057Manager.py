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
        self._warnValue = IntVar()
        self._critValue = IntVar()
        self._warnColor = None
        self._critColor = None

        lbl = ttk.Label(self, text="Начальное значения для Предупреждения")
        lbl.grid(row=0, column=0, padx=2, pady=2)

        ttk.Entry(self, textvariable=self._warnValue, width=4).grid(row=0, column=1, padx=2, pady=2)

        lbl = ttk.Label(self, text="Цвет текста для Предупреждения")
        lbl.grid(row=1, column=0, padx=2, pady=2)

        self._warnSelector = Button(self, text="Предупреждение", command=self._selectWarnColor)
        self._warnSelector.grid(row=1, column=1, padx=2, pady=2, sticky=(N, S, E, W))

        lbl = ttk.Label(self, text="Начальное значения для Опасности")
        lbl.grid(row=2, column=0, padx=2, pady=2)

        ttk.Entry(self, textvariable=self._critValue, width=4).grid(row=2, column=1, padx=2, pady=2)

        lbl = ttk.Label(self, text="Цвет текста для Опасности")
        lbl.grid(row=3, column=0, padx=2, pady=2)

        self._critSelector = Button(self, text="Опасность", command=self._selectCritColor)
        self._critSelector.grid(row=3, column=1, padx=2, pady=2, sticky=(N, S, E, W))

        self._posCO2 = XYFrame(self, "Расположение CO2", "Расположение (X)", "Расположение (Y)")
        self._posCO2.grid(row=4, column=0, columnspan=2, padx=2, pady=2, sticky=(N, S, E, W))

        self._posTemp = XYFrame(self, "Расположение Температуры", "Расположение (X)", "Расположение (Y)")
        self._posTemp.grid(row=5, column=0, columnspan=2, padx=2, pady=2, sticky=(N, S, E, W))

        self._co2 = FontChooserFrame(self, "Параметры шрифта CO2")
        self._co2.grid(row=6, column=0, columnspan=2, padx=2, pady=2, sticky=(N, S, E, W))

        self._temp = FontChooserFrame(self, "Параметры шрифта Температуры")
        self._temp.grid(row=7, column=0, columnspan=2, padx=2, pady=2, sticky=(N, S, E, W))

    def load(self, config, modulelist):
        if not isinstance(config, configparser.ConfigParser):
            raise TypeError("config")
        if not config.has_section("MT8057Block"):
            config.add_section("MT8057Block")
        section = config["MT8057Block"]
        self._warnValue.set(section.getint("Warn", 800))
        self._critValue.set(section.getint("Crit", 1200))
        self._warnColor = self._getTuple(section.get("WarnColor", "(255, 127, 0)"))
        self._critColor = self._getTuple(section.get("CritColor", "(255, 63, 63)"))

        fontName = section.get("CO2FontName", "Helvetica")
        fontSize = section.getint("CO2FontSize", 100)
        isBold = section.getboolean("CO2FontBold", True)
        isItalic = section.getboolean("CO2FontItalic", False)
        self._co2.load(fontName, fontSize, isBold, isItalic)

        fontName = section.get("TempFontName", "Helvetica")
        fontSize = section.getint("TempFontSize", 100)
        isBold = section.getboolean("TempFontBold", True)
        isItalic = section.getboolean("TempFontItalic", False)
        self._temp.load(fontName, fontSize, isBold, isItalic)

        (posX, posY) = self._getTuple(section.get("CO2Pos", "(0, 0)"))
        self._posCO2.load(posX, posY)
        (posX, posY) = self._getTuple(section.get("TempPos", "(0, 0)"))
        self._posTemp.load(posX, posY)

        self._warnSelector.configure(foreground="#%02x%02x%02x" % self._warnColor)
        self._critSelector.configure(foreground="#%02x%02x%02x" % self._critColor)

    def save(self, config):
        if not isinstance(config, configparser.ConfigParser):
            raise TypeError("config")
        if not config.has_section("MT8057Block"):
            config.add_section("MT8057Block")
        section = config["MT8057Block"]
        section["Warn"] = str(self._warnValue.get())
        section["Crit"] = str(self._critValue.get())
        section["WarnColor"] = "(%d, %d, %d)" % self._warnColor
        section["CritColor"] = "(%d, %d, %d)" % self._critColor

        (fontName, fontSize, isBold, isItalic) = self._co2.getResult()
        section["CO2FontName"] = fontName
        section["CO2FontSize"] = str(fontSize)
        section["CO2FontBold"] = str(isBold)
        section["CO2FontItalic"] = str(isItalic)

        (fontName, fontSize, isBold, isItalic) = self._temp.getResult()
        section["TempFontName"] = fontName
        section["TempFontSize"] = str(fontSize)
        section["TempFontBold"] = str(isBold)
        section["TempFontItalic"] = str(isItalic)

        (posX, posY) = self._posCO2.getResult()
        section["CO2Pos"] = "({0},{1})".format(posX, posY)
        (posX, posY) = self._posTemp.getResult()
        section["TempPos"] = "({0},{1})".format(posX, posY)

    def _selectWarnColor(self):
        (tripleColor, tkColor) = colorchooser.askcolor(self._warnColor)
        if tripleColor is None:
            return
        self._warnSelector.configure(foreground=tkColor)
        self._warnColor = (int(tripleColor[0]), int(tripleColor[1]), int(tripleColor[2]))

    def _selectCritColor(self):
        (tripleColor, tkColor) = colorchooser.askcolor(self._critColor)
        if tripleColor is None:
            return
        self._critSelector.configure(foreground=tkColor)
        self._critColor = (int(tripleColor[0]), int(tripleColor[1]), int(tripleColor[2]))

    def _getTuple(self, value):
        """  Конвертирует строку '0, 0, 0' в кортеж (0, 0, 0) """
        try:
            return tuple(int(item.strip("([ '])")) for item in value.split(",") if item.strip())
        except Exception as ex:
            return None
