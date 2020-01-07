from typing import Dict
from configparser import ConfigParser
from tkinter import IntVar, StringVar, LabelFrame, Label, Entry, Spinbox, N, S, E, W
from tkinter.ttk import Combobox
from ext.base_manager import BaseManager
from ext.modal_dialog import SelectFrame

VOICE_LIST = ('alena', 'filipp', 'ermil', 'jane', 'oksana', 'omazh', 'zahar')


class VoiceManager(BaseManager):
    """description of class"""

    def __init__(self, root: LabelFrame):
        """ """
        super(VoiceManager, self).__init__(root, text="Настройки голосового модуля")
        self._speaker_value = StringVar()
        self._key_value = StringVar()
        self._speed_value = IntVar()

        lbl = Label(self, text="Голос")
        lbl.grid(row=0, column=0, padx=2, pady=2)

        combo = Combobox(self, state="readonly", values=VOICE_LIST, textvariable=self._speaker_value)
        combo.grid(row=0, column=1, padx=2, pady=2)

        lbl = Label(self, text="Скорость (0-30)")
        lbl.grid(row=0, column=2, padx=2, pady=2)

        spin = Spinbox(self, from_=0, to=30, increment=1, width=3, textvariable=self._speed_value)
        spin.grid(row=0, column=3, padx=2, pady=2)

        lbl = Label(self, text="Яндекс ключ")
        lbl.grid(row=1, column=0, padx=2, pady=2)

        entr = Entry(self, textvariable=self._key_value, width=35)
        entr.grid(row=1, column=1, columnspan=3, sticky=(N, S, E, W), padx=2, pady=2)

        self._frame = SelectFrame(self, "Выбор модулей")
        self._frame.grid(row=2, column=0, columnspan=4, sticky=(N, S, E, W), padx=2, pady=2)

    def load(self, config: ConfigParser, module_list: Dict[str, BaseManager]) -> None:
        if not isinstance(config, ConfigParser):
            raise TypeError("config")
        if not config.has_section("VoiceBlock"):
            config.add_section("VoiceBlock")
        section = config["VoiceBlock"]
        self._speaker_value.set(section.get("Speaker", fallback="omazh"))
        self._speed_value.set(int(section.getfloat("Speed", fallback=1.0) * 10))
        self._key_value.set(section.get("Key", fallback=""))
        selection = [item.strip(" '") for item in section.get("BlockList", fallback="").split(",")
                    if item.strip() in module_list]
        self._frame.load(selection, module_list)

    def save(self, config: ConfigParser) -> None:
        if not isinstance(config, ConfigParser):
            raise TypeError("config")
        if not config.has_section("VoiceBlock"):
            config.add_section("VoiceBlock")
        section = config["VoiceBlock"]
        section["Speaker"] = self._speaker_value.get()
        section["Speed"] = str(self._speed_value.get() / 10)
        section["Key"] = self._key_value.get()
        section["BlockList"] = self._frame.get_result()
