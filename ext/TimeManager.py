import configparser

from tkinter import *
from tkinter import font
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import colorchooser

class TimeManager(ttk.LabelFrame):
    """description of class"""

    def __init__(self, root):
        """ """
        super(TimeManager, self).__init__(root, text="Настройки часов")
        self._fontName = StringVar()
        self._fontSize = IntVar()
        self._isBold = BooleanVar()
        self._isItalic = BooleanVar()
        ttk.Label(self, text="Шрифт").grid(row=0, column=0, padx=2, pady=2)
        fonts = list(font.families())
        list.sort(fonts)
        ttk.Combobox(self, values=fonts, textvariable=self._fontName).grid(row=0, column=1, padx=2, pady=2)
        ttk.Label(self, text="Размер").grid(row=0, column=2, padx=2, pady=2)
        Spinbox(self, from_=1, to=500, increment=1, width=4, textvariable=self._fontSize).grid(row=0, column=3, padx=2, pady=2)
        ttk.Checkbutton(self, text="Жирный", variable=self._isBold).grid(row=0, column=4, padx=2, pady=2)
        ttk.Checkbutton(self, text="Наклон", variable=self._isItalic).grid(row=0, column=5, padx=2, pady=2)
        

    def load(self, config):
        if not isinstance(config, configparser.ConfigParser): raise TypeError("config")
        section = config["TimeBlock"]
        fontName = section.get("FontName", "Helvetica")
        fontSize = section.getint("FontSize", 384)
        isBold = section.getboolean("FontBold", True)
        isItalic = section.getboolean("FontItalic", False)
        self._fontName.set(fontName)
        self._fontSize.set(fontSize)
        self._isBold.set(isBold)
        self._isItalic.set(isItalic)

    def save(self, config):
        if not isinstance(config, configparser.ConfigParser): raise TypeError("config")
        if not config.has_section("TimeBlock"):      config.add_section("TimeBlock")
        section = config["TimeBlock"]
        section["FontName"] = self._fontName.get()
        section["FontSize"] = str(self._fontSize.get())
        section["FontBold"] = str(self._isBold.get())
        section["FontItalic"] = str(self._isItalic.get())

