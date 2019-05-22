from typing import Dict
from configparser import ConfigParser
from tkinter import StringVar, LabelFrame, Label, Entry, N, S, E, W
from tkinter.ttk import Combobox
from ext.base_manager import BaseManager
from ext.modal_dialog import SelectFrame

VOICE_LIST = ('jane', 'oksana', 'alyss', 'omazh', 'zahar', 'ermil')


class VoiceManager(BaseManager):
    """description of class"""

    def __init__(self, root: LabelFrame):
        """ """
        super(VoiceManager, self).__init__(root, text="Настройки голосового модуля")
        self._speaker_value = StringVar()
        self._key_value = StringVar()

        lbl = Label(self, text="Голос")
        lbl.grid(row=0, column=0, padx=2, pady=2)

        combo = Combobox(self, state="readonly", values=VOICE_LIST, textvariable=self._speaker_value)
        combo.grid(row=0, column=1, padx=2, pady=2)

        lbl = Label(self, text="Яндекс ключ")
        lbl.grid(row=0, column=2, padx=2, pady=2)

        entr = Entry(self, textvariable=self._key_value, width=35)
        entr.grid(row=0, column=3, padx=2, pady=2)

        self._frame = SelectFrame(self, "Выбор модулей")
        self._frame.grid(row=1, column=0, columnspan=4, sticky=(N, S, E, W), padx=2, pady=2)

    def load(self, config: ConfigParser, module_list: Dict[str, BaseManager]) -> None:
        if not isinstance(config, ConfigParser):
            raise TypeError("config")
        if not config.has_section("VoiceBlock"):
            config.add_section("VoiceBlock")
        section = config["VoiceBlock"]
        self._speaker_value.set(section.get("Speaker", fallback="omazh"))
        self._key_value.set(section.get("Key", fallback=""))
        selection = [item.strip(" '") for item in section.get("BlockList", fallback="").split(",") if item.strip() in module_list]
        self._frame.load(selection, module_list)

    def save(self, config: ConfigParser) -> None:
        if not isinstance(config, ConfigParser):
            raise TypeError("config")
        if not config.has_section("VoiceBlock"):
            config.add_section("VoiceBlock")
        section = config["VoiceBlock"]
        section["Speaker"] = self._speaker_value.get()
        section["Key"] = self._key_value.get()
        section["BlockList"] = self._frame.get_result()
