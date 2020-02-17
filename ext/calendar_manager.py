from typing import Dict
from configparser import ConfigParser
from tkinter import StringVar, Entry, LabelFrame, Label, N, S, E, W, RIGHT
from ext.base_manager import BaseManager
from ext.modal_dialog import DisplayTextFrame

class CalendarManager(BaseManager):
    """description of class"""

    def __init__(self, root: LabelFrame):
        """ """
        super(CalendarManager, self).__init__(root, text="Настройки календаря, Параметры: "
                                                         "День={0}, Месяц={1}, Год={2}, Нед. кор.={3}, Нед. полная={4}")
        self._format_text_value = StringVar()

        lbl = Label(self, justify=RIGHT, text="Формат текста")
        lbl.grid(row=0, column=0, padx=2, pady=2, sticky=(N, S, E))
        entr = Entry(self, width=60, textvariable=self._format_text_value)
        entr.grid(row=0, column=1, padx=2, pady=2, sticky=(N, S, E, W))

        self._calendar = DisplayTextFrame(self, "", "")
        self._calendar.grid(row=1, column=0, columnspan=2, sticky=(N, S, E, W))

    def load(self, config: ConfigParser, module_list: Dict[str, BaseManager]) -> None:
        if not isinstance(config, ConfigParser):
            raise TypeError("config")
        if not config.has_section("CalendarBlock"):
            config.add_section("CalendarBlock")
        section = config["CalendarBlock"]
        self._format_text_value.set(section.get("FormatText", fallback=""))
        self._calendar.load(section)

    def save(self, config: ConfigParser) -> None:
        if not isinstance(config, ConfigParser):
            raise TypeError("config")
        if not config.has_section("CalendarBlock"):
            config.add_section("CalendarBlock")
        section = config["CalendarBlock"]
        section["FormatText"] = self._format_text_value.get()
        self._calendar.save(section)
