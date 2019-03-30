from typing import *

from configparser import ConfigParser
from tkinter import *

from ext.BaseManager import BaseManager
from ext.ModalDialog import FontChooserFrame


class TimeManager(BaseManager):
    """description of class"""

    def __init__(self, root: LabelFrame):
        """ """
        super(TimeManager, self).__init__(root, text="Настройки часов")
        self._font = FontChooserFrame(self, "Параметры шрифта")
        self._font.grid(row=0, column=1)

    def load(self, config: ConfigParser, modulelist: Dict[str, BaseManager]) -> None:
        if not isinstance(config, ConfigParser):
            raise TypeError("config")
        if not config.has_section("TimeBlock"):
            config.add_section("TimeBlock")
        section = config["TimeBlock"]
        fontName = section.get("FontName", "Helvetica")
        fontSize = section.getint("FontSize", 384)
        isBold = section.getboolean("FontBold", True)
        isItalic = section.getboolean("FontItalic", False)
        self._font.load(fontName, fontSize, isBold, isItalic)

    def save(self, config: ConfigParser) -> None:
        if not isinstance(config, ConfigParser):
            raise TypeError("config")
        if not config.has_section("TimeBlock"):
            config.add_section("TimeBlock")
        section = config["TimeBlock"]
        (fontName, fontSize, isBold, isItalic) = self._font.getResult()
        section["FontName"] = fontName
        section["FontSize"] = str(fontSize)
        section["FontBold"] = str(isBold)
        section["FontItalic"] = str(isItalic)
