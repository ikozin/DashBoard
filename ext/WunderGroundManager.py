import configparser

from tkinter import *
from tkinter import font
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import colorchooser

from ext.ModalDialog import FontChooserFrame
from ext.ModalDialog import XYFrame

class WunderGroundManager(ttk.LabelFrame):
    """description of class"""

    def __init__(self, root):
        """ """
        super(WunderGroundManager, self).__init__(root, text="Настройки WunderGround")

        self._updateValue = IntVar()
        self._keyValue = StringVar()
        self._folderValue = StringVar()

        content = ttk.Frame(self)
        content.grid(row=0, column=0, padx=2, pady=2, sticky=(N,S,E,W))
        
        ttk.Label(content, justify=RIGHT, text="Время обновления").grid(row=0, column=0, padx=2, pady=2, sticky=(N,S,E))
        Spinbox(content, from_=1, to=60, increment=1, width=5, textvariable=self._updateValue).grid(row=0, column=1, padx=2, pady=2, sticky=(N,S,E,W))
        ttk.Label(content, justify=LEFT, text="минут").grid(row=0, column=2, padx=2, pady=2, sticky=(N,S,W))
        
        ttk.Label(content, justify=RIGHT, text="Ключ").grid(row=1, column=0, padx=2, pady=2, sticky=(N,S,E))
        ttk.Entry(content, width=40, textvariable=self._keyValue).grid(row=1, column=1, columnspan=2, padx=2, pady=2, sticky=(N,S,E,W))
        
        ttk.Label(content, justify=RIGHT, text="Директория для картинок").grid(row=2, column=0, padx=2, pady=2, sticky=(N,S,E))
        ttk.Entry(content, width=5, textvariable=self._folderValue).grid(row=2, column=1, columnspan=2, padx=2, pady=2, sticky=(N,S,E,W))

        self._scaleIcon = XYFrame(self, "Масштаб для картинки", "Масштаб (X)", "Масштаб (Y)")
        self._scaleIcon.grid(row=1, column=0, padx=2, pady=2, sticky=(N,S,E,W))
        self._posIcon = XYFrame(self, "Расположение для картинки", "Расположение (X)", "Расположение (Y)")
        self._posIcon.grid(row=2, column=0, padx=2, pady=2, sticky=(N,S,E,W))

        self._posWeatherType = XYFrame(self, "Расположение для погоды", "Расположение (X)", "Расположение (Y)")
        self._posWeatherType.grid(row=3, column=0, padx=2, pady=2, sticky=(N,S,E,W))
        self._posTemperature = XYFrame(self, "Расположение для температуры", "Расположение (X)", "Расположение (Y)")
        self._posTemperature.grid(row=4, column=0, padx=2, pady=2, sticky=(N,S,E,W))
        self._posHumidity = XYFrame(self, "Расположение для влажности", "Расположение (X)", "Расположение (Y)")
        self._posHumidity.grid(row=5, column=0, padx=2, pady=2, sticky=(N,S,E,W))
        self._posPressure = XYFrame(self, "Расположение для давления", "Расположение (X)", "Расположение (Y)")
        self._posPressure.grid(row=6, column=0, padx=2, pady=2, sticky=(N,S,E,W))
        self._posWind = XYFrame(self, "Расположение для ветра", "Расположение (X)", "Расположение (Y)")
        self._posWind.grid(row=7, column=0, padx=2, pady=2, sticky=(N,S,E,W))

        self._weatherType = FontChooserFrame(self, "Параметры шрифта для погоды")
        self._weatherType.grid(row=8, column=0, padx=2, pady=2, sticky=(N,S,E,W))
        self._temperature = FontChooserFrame(self, "Параметры шрифта для температуры")
        self._temperature.grid(row=9, column=0, padx=2, pady=2, sticky=(N,S,E,W))
        self._humidity = FontChooserFrame(self, "Параметры шрифта для влажности")
        self._humidity.grid(row=10, column=0, padx=2, pady=2, sticky=(N,S,E,W))
        self._pressure = FontChooserFrame(self, "Параметры шрифта для давления")
        self._pressure.grid(row=11, column=0, padx=2, pady=2, sticky=(N,S,E,W))
        self._wind = FontChooserFrame(self, "Параметры шрифта ветра")
        self._wind.grid(row=12, column=0, padx=2, pady=2, sticky=(N,S,E,W))


    def load(self, config):
        """ """
        if not isinstance(config, configparser.ConfigParser): raise TypeError("config")
        if not config.has_section("WunderGroundBlock"):      config.add_section("WunderGroundBlock")
        section = config["WunderGroundBlock"]

        self._updateValue.set(section.getint("UpdateTime", 15))
        self._keyValue.set(section.get("Key", ""))
        self._folderValue.set(section.get("Folder", ""))

        (posX, posY) = self._getTuple(section.get("IconScale", "(256, 256)"))
        self._scaleIcon.load(posX, posY)
        (posX, posY) = self._getTuple(section.get("IconPos", "(0, 0)"))
        self._posIcon.load(posX, posY)
        
        (posX, posY) = self._getTuple(section.get("WeatherTypePos", "(260, 242)"))
        self._posWeatherType.load(posX, posY)
        (posX, posY) = self._getTuple(section.get("TemperaturePos", "(240, 50)"))
        self._posTemperature.load(posX, posY)
        (posX, posY) = self._getTuple(section.get("HumidityPos", "(620, 98)"))
        self._posHumidity.load(posX, posY)
        (posX, posY) = self._getTuple(section.get("PressurePos", "(620, 170)"))
        self._posPressure.load(posX, posY)
        (posX, posY) = self._getTuple(section.get("WindPos", "(620, 26)"))
        self._posWind.load(posX, posY)

        fontName = section.get("WeatherTypeFontName", "Helvetica")
        fontSize = section.getint("WeatherTypeFontSize", 64)
        isBold = section.getboolean("WeatherTypeFontBold", True)
        isItalic = section.getboolean("WeatherTypeFontItalic", False)
        self._weatherType.load(fontName, fontSize, isBold, isItalic)

        fontName = section.get("TemperatureFontName", "Helvetica")
        fontSize = section.getint("TemperatureFontSize", 160)
        isBold = section.getboolean("TemperatureFontBold", True)
        isItalic = section.getboolean("TemperatureFontItalic", False)
        self._temperature.load(fontName, fontSize, isBold, isItalic)

        fontName = section.get("HumidityFontName", "Helvetica")
        fontSize = section.getint("HumidityFontSize", 64)
        isBold = section.getboolean("HumidityFontBold", False)
        isItalic = section.getboolean("HumidityFontItalic", False)
        self._humidity.load(fontName, fontSize, isBold, isItalic)

        fontName = section.get("PressureFontName", "Helvetica")
        fontSize = section.getint("PressureFontSize", 64)
        isBold = section.getboolean("PressureFontBold", False)
        isItalic = section.getboolean("PressureFontItalic", False)
        self._pressure.load(fontName, fontSize, isBold, isItalic)

        fontName = section.get("WindFontName", "Helvetica")
        fontSize = section.getint("WindFontSize", 64)
        isBold = section.getboolean("WindFontBold", False)
        isItalic = section.getboolean("WindFontItalic", False)
        self._wind.load(fontName, fontSize, isBold, isItalic)


    def save(self, config):
        """ """
        if not isinstance(config, configparser.ConfigParser): raise TypeError("config")
        if not config.has_section("WunderGroundBlock"):      config.add_section("WunderGroundBlock")
        section = config["WunderGroundBlock"]

        section["UpdateTime"] = str(self._updateValue.get())
        section["Key"] = self._keyValue.get()
        section["Folder"] = self._folderValue.get()

        (posX, posY) = self._scaleIcon.getResult()
        section["IconScale"] = "({0},{1})".format(posX, posY)
        (posX, posY) = self._posIcon.getResult()
        section["IconPos"] = "({0},{1})".format(posX, posY)

        (posX, posY) = self._posWeatherType.getResult()
        section["WeatherTypePos"] = "({0},{1})".format(posX, posY)
        (posX, posY) = self._posTemperature.getResult()
        section["TemperaturePos"] = "({0},{1})".format(posX, posY)
        (posX, posY) = self._posHumidity.getResult()
        section["HumidityPos"] = "({0},{1})".format(posX, posY)
        (posX, posY) = self._posPressure.getResult()
        section["PressurePos"] = "({0},{1})".format(posX, posY)
        (posX, posY) = self._posWind.getResult()
        section["WindPos"] = "({0},{1})".format(posX, posY)

        (fontName, fontSize, isBold, isItalic) = self._weatherType.getResult()
        section["WeatherTypeFontName"]   = fontName
        section["WeatherTypeFontSize"]   = str(fontSize)
        section["WeatherTypeFontBold"]   = str(isBold)
        section["WeatherTypeFontItalic"] = str(isItalic)

        (fontName, fontSize, isBold, isItalic) = self._temperature.getResult()
        section["TemperatureFontName"]   = fontName
        section["TemperatureFontSize"]   = str(fontSize)
        section["TemperatureFontBold"]   = str(isBold)
        section["TemperatureFontItalic"] = str(isItalic)

        (fontName, fontSize, isBold, isItalic) = self._humidity.getResult()
        section["HumidityFontName"]   = fontName
        section["HumidityFontSize"]   = str(fontSize)
        section["HumidityFontBold"]   = str(isBold)
        section["HumidityFontItalic"] = str(isItalic)

        (fontName, fontSize, isBold, isItalic) = self._pressure.getResult()
        section["PressureFontName"]   = fontName
        section["PressureFontSize"]   = str(fontSize)
        section["PressureFontBold"]   = str(isBold)
        section["PressureFontItalic"] = str(isItalic)

        (fontName, fontSize, isBold, isItalic) = self._wind.getResult()
        section["WindFontName"]   = fontName
        section["WindFontSize"]   = str(fontSize)
        section["WindFontBold"]   = str(isBold)
        section["WindFontItalic"] = str(isItalic)


    def _getTuple(self, value):
        """  Конвертирует строку '0, 0, 0' в кортеж (0, 0, 0) """
        try:
            return tuple(int(item.strip("([ '])")) for item in value.split(",") if item.strip())
        except Exception as ex:
            return None


