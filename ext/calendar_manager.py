from typing import Dict
from configparser import ConfigParser
from tkinter import IntVar, StringVar, Entry, LabelFrame, Label, Spinbox, N, S, E, W, RIGHT
from tkinter.ttk import Frame
from ext.base_manager import BaseManager
from ext.modal_dialog import FontChooserFrame


class CalendarManager(BaseManager):
    """description of class"""

    def __init__(self, root: LabelFrame):
        """ """
        super(CalendarManager, self).__init__(root, text="Настройки календаря, Параметры: "
                                                         "День={0}, Месяц={1}, Год={2}, Нед. кор.={3}, Нед. полная={4}")
        self._pos_value = IntVar()
        self._format_date_value = StringVar()
        self._format_text_value = StringVar()

        content = Frame(self)
        content.grid(row=0, column=0, columnspan=2, padx=2, pady=2, sticky=(N, S, E, W))
        lbl = Label(content, text="Распложение (Y)")
        lbl.grid(row=0, column=0, padx=2, pady=2)
        spin = Spinbox(content, from_=1, to=1000, increment=1, width=5, textvariable=self._pos_value)
        spin.grid(row=0, column=1, padx=2, pady=2)
        self._font = FontChooserFrame(self, "Параметры шрифта")
        self._font.grid(row=1, column=0, columnspan=2, padx=2, pady=2, sticky=(N, S, E, W))
        lbl = Label(self, justify=RIGHT, text="Отображение")
        lbl.grid(row=2, column=0, padx=2, pady=2, sticky=(N, S, E))
        entr = Entry(self, width=60, textvariable=self._format_date_value)
        entr.grid(row=2, column=1, padx=2, pady=2, sticky=(N, S, E, W))
        lbl = Label(self, justify=RIGHT, text="Формат текста")
        lbl.grid(row=3, column=0, padx=2, pady=2, sticky=(N, S, E))
        entr = Entry(self, width=60, textvariable=self._format_text_value)
        entr.grid(row=3, column=1, padx=2, pady=2, sticky=(N, S, E, W))

    def load(self, config: ConfigParser, module_list: Dict[str, BaseManager]) -> None:
        if not isinstance(config, ConfigParser):
            raise TypeError("config")
        if not config.has_section("CalendarBlock"):
            config.add_section("CalendarBlock")
        section = config["CalendarBlock"]
        font_name = section.get("FontName", fallback="Helvetica")
        font_size = section.getint("FontSize", fallback=150)
        is_bold = section.getboolean("FontBold", fallback=True)
        is_italic = section.getboolean("FontItalic", fallback=False)
        self._font.load(font_name, font_size, is_bold, is_italic)
        self._pos_value.set(section.getint("Position", fallback=80))
        self._format_date_value.set(section.get("Format", fallback=""))
        self._format_text_value.set(section.get("FormatText", fallback=""))

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
        section["Format"] = self._format_date_value.get()
        section["FormatText"] = self._format_text_value.get()
