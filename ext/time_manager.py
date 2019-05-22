from typing import Dict
from configparser import ConfigParser
from tkinter import LabelFrame
from ext.base_manager import BaseManager
from ext.modal_dialog import FontChooserFrame


class TimeManager(BaseManager):
    """description of class"""

    def __init__(self, root: LabelFrame):
        """ """
        super(TimeManager, self).__init__(root, text="Настройки часов")
        self._font = FontChooserFrame(self, "Параметры шрифта")
        self._font.grid(row=0, column=1)

    def load(self, config: ConfigParser, module_list: Dict[str, BaseManager]) -> None:
        if not isinstance(config, ConfigParser):
            raise TypeError("config")
        if not config.has_section("TimeBlock"):
            config.add_section("TimeBlock")
        section = config["TimeBlock"]
        font_name = section.get("FontName", fallback="Helvetica")
        font_size = section.getint("FontSize", fallback=384)
        is_bold = section.getboolean("FontBold", fallback=True)
        is_italic = section.getboolean("FontItalic", fallback=False)
        self._font.load(font_name, font_size, is_bold, is_italic)

    def save(self, config: ConfigParser) -> None:
        if not isinstance(config, ConfigParser):
            raise TypeError("config")
        if not config.has_section("TimeBlock"):
            config.add_section("TimeBlock")
        section = config["TimeBlock"]
        (font_name, font_size, is_bold, is_italic) = self._font.get_result()
        section["FontName"] = font_name
        section["FontSize"] = str(font_size)
        section["FontBold"] = str(is_bold)
        section["FontItalic"] = str(is_italic)
