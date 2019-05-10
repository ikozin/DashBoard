from typing import Dict
from configparser import ConfigParser
from tkinter import IntVar, LabelFrame, Label, Spinbox, N, S, E, W
from tkinter.ttk import Frame
from ext.base_manager import BaseManager
from ext.modal_dialog import FontChooserFrame


class CalendarManager(BaseManager):
    """description of class"""

    def __init__(self, root: LabelFrame):
        """ """
        super(CalendarManager, self).__init__(root, text="Настройки календаря")
        self._pos_value = IntVar()
        content = Frame(self)
        content.grid(row=0, column=0, padx=2, pady=2, sticky=(N, S, E, W))
        lbl = Label(content, text="Распложение (Y)")
        lbl.grid(row=0, column=0, padx=2, pady=2)
        spin = Spinbox(content, from_=1, to=1000, increment=1, width=5, textvariable=self._pos_value)
        spin.grid(row=0, column=1, padx=2, pady=2)
        self._font = FontChooserFrame(self, "Параметры шрифта")
        self._font.grid(row=1, column=0, padx=2, pady=2, sticky=(N, S, E, W))

    def load(self, config: ConfigParser, module_list: Dict[str, BaseManager]) -> None:
        if not isinstance(config, ConfigParser):
            raise TypeError("config")
        if not config.has_section("CalendarBlock"):
            config.add_section("CalendarBlock")
        section = config["CalendarBlock"]
        font_name = section.get("FontName", "Helvetica")
        font_size = section.getint("FontSize", 150)
        is_bold = section.getboolean("FontBold", True)
        is_italic = section.getboolean("FontItalic", False)
        self._font.load(font_name, font_size, is_bold, is_italic)
        self._pos_value.set(section.getint("Position", 80))

    def save(self, config: ConfigParser) -> None:
        if not isinstance(config, ConfigParser):
            raise TypeError("config")
        if not config.has_section("CalendarBlock"):
            config.add_section("CalendarBlock")
        section = config["CalendarBlock"]
        (font_name, font_size, is_bold, is_italic) = self._font.get_result()
        section["FontName"] = font_name
        section["FontSize"] = str(font_size)
        section["FontBold"] = str(is_bold)
        section["FontItalic"] = str(is_italic)
        section["Position"] = str(self._pos_value.get())
