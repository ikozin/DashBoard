from typing import Dict
from configparser import ConfigParser
from tkinter import StringVar, Entry, LabelFrame, Label, N, S, E, W, RIGHT
from ext.base_manager import BaseManager
from ext.modal_dialog import DisplayTextFrame


class TimeManager(BaseManager):
    """description of class"""

    def __init__(self, root: LabelFrame):
        """ """
        super(TimeManager, self).__init__(root, text="Настройки часов")
        self._format_text_value = StringVar()

        lbl = Label(self, justify=RIGHT, text="Формат текста")
        lbl.grid(row=0, column=0, padx=2, pady=2, sticky=(N, S, E))
        entr = Entry(self, width=60, textvariable=self._format_text_value)
        entr.grid(row=0, column=1, padx=2, pady=2, sticky=(N, S, E, W))

        self._time = DisplayTextFrame(self, "Параметр Время", "")
        self._time.grid(row=1, column=0, columnspan=2, sticky=(N, S, E, W))

    def load(self, config: ConfigParser, module_list: Dict[str, BaseManager]) -> None:
        if not isinstance(config, ConfigParser):
            raise TypeError("config")
        if not config.has_section("TimeBlock"):
            config.add_section("TimeBlock")
        section = config["TimeBlock"]
        self._format_text_value.set(section.get("FormatText", fallback=""))
        self._time.load(section)

    def save(self, config: ConfigParser) -> None:
        if not isinstance(config, ConfigParser):
            raise TypeError("config")
        if not config.has_section("TimeBlock"):
            config.add_section("TimeBlock")
        section = config["TimeBlock"]
        section["FormatText"] = self._format_text_value.get()
        self._time.save(section)
