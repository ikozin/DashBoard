import configparser

from tkinter import *
from tkinter import font
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import colorchooser

from ext.ModalDialog import FontChooserFrame

class TimeManager(ttk.LabelFrame):
    """description of class"""

    def __init__(self, root):
        """ """
        super(TimeManager, self).__init__(root, text="Настройки часов")
        self._font = FontChooserFrame(self, "Параметры шрифта")
        self._font.grid(row=0, column=1)

    def load(self, config, modulelist):
        if not isinstance(config, configparser.ConfigParser): raise TypeError("config")
        if not config.has_section("TimeBlock"):      config.add_section("TimeBlock")
        section = config["TimeBlock"]
        fontName = section.get("FontName", "Helvetica")
        fontSize = section.getint("FontSize", 384)
        isBold = section.getboolean("FontBold", True)
        isItalic = section.getboolean("FontItalic", False)
        self._font.load(fontName, fontSize, isBold, isItalic)

    def save(self, config):
        if not isinstance(config, configparser.ConfigParser): raise TypeError("config")
        if not config.has_section("TimeBlock"):      config.add_section("TimeBlock")
        section = config["TimeBlock"]
        (fontName, fontSize, isBold, isItalic) = self._font.getResult()
        section["FontName"]   = fontName
        section["FontSize"]   = str(fontSize)
        section["FontBold"]   = str(isBold)
        section["FontItalic"] = str(isItalic)

