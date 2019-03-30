from typing import *

from configparser import ConfigParser
from tkinter import *

from ext.BaseManager import BaseManager
from ext.ModalDialog import FontChooserFrame


class CalendarManager(BaseManager):
    """description of class"""

    def __init__(self, root: LabelFrame):
        """ """
        super(CalendarManager, self).__init__(root, text="Настройки календаря")
        self._posValue = IntVar()

        content = Frame(self)
        content.grid(row=0, column=0, padx=2, pady=2, sticky=(N, S, E, W))

        lbl = Label(content, text="Распложение (Y)")
        lbl.grid(row=0, column=0, padx=2, pady=2)

        spin = Spinbox(content, from_=1, to=1000, increment=1, width=5, textvariable=self._posValue)
        spin.grid(row=0, column=1, padx=2, pady=2)

        self._font = FontChooserFrame(self, "Параметры шрифта")
        self._font.grid(row=1, column=0, padx=2, pady=2, sticky=(N, S, E, W))

    def load(self, config: ConfigParser, modulelist: Dict[str, BaseManager]) -> None:
        if not isinstance(config, ConfigParser):
            raise TypeError("config")
        if not config.has_section("CalendarBlock"):
            config.add_section("CalendarBlock")
        section = config["CalendarBlock"]
        fontName = section.get("FontName", "Helvetica")
        fontSize = section.getint("FontSize", 150)
        isBold = section.getboolean("FontBold", True)
        isItalic = section.getboolean("FontItalic", False)
        self._font.load(fontName, fontSize, isBold, isItalic)
        self._posValue.set(section.getint("Position", 80))

    def save(self, config: ConfigParser) -> None:
        if not isinstance(config, ConfigParser):
            raise TypeError("config")
        if not config.has_section("CalendarBlock"):
            config.add_section("CalendarBlock")
        section = config["CalendarBlock"]
        (fontName, fontSize, isBold, isItalic) = self._font.getResult()
        section["FontName"] = fontName
        section["FontSize"] = str(fontSize)
        section["FontBold"] = str(isBold)
        section["FontItalic"] = str(isItalic)
        section["Position"] = str(self._posValue.get())
