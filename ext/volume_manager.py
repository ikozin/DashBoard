from typing import Dict
from configparser import ConfigParser
from tkinter import IntVar, LabelFrame, Label, Spinbox, LEFT, N, S, E, W
from ext.base_manager import BaseManager
from ext.modal_dialog import DisplayTextFrame


class VolumeManager(BaseManager):
    """description of class"""

    def __init__(self, root: LabelFrame):
        """ """
        super(VolumeManager, self).__init__(root, text="Настройки модуля громкости")
        self._volume_value = IntVar()

        lbl = Label(self, justify=LEFT, text="Поддерживает следующие команды\n"
                    "'+' - увеличить громкость\n"
                    "'-' - уменьшить громкость\n"
                    "'on' - включить громкость\n"
                    "'off' - выключить громкость")
        lbl.grid(row=0, column=0, columnspan=2, padx=2, pady=2)

        lbl = Label(self, text="Громкость (0-100)%")
        lbl.grid(row=1, column=0, padx=2, pady=2)

        spin = Spinbox(self, from_=0, to=100, increment=1, width=4, textvariable=self._volume_value)
        spin.grid(row=1, column=1, padx=2, pady=2)

        self._text = DisplayTextFrame(self, "Громкость", "")
        self._text.grid(row=2, column=0, columnspan=2, padx=2, pady=2, sticky=(N, S, E, W))


    def load(self, config: ConfigParser, module_list: Dict[str, BaseManager]) -> None:
        if not isinstance(config, ConfigParser):
            raise TypeError("config")
        if not config.has_section("VolumeBlock"):
            config.add_section("VolumeBlock")
        section = config["VolumeBlock"]
        self._volume_value.set(int(section.getfloat("Volume", fallback=50)))
        self._text.load(section)

    def save(self, config: ConfigParser) -> None:
        if not isinstance(config, ConfigParser):
            raise TypeError("config")
        if not config.has_section("VolumeBlock"):
            config.add_section("VolumeBlock")
        section = config["VolumeBlock"]
        section["Volume"] = str(self._volume_value.get())
        self._text.save(section)
