import configparser

from tkinter import *
from tkinter import font
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import colorchooser

from ext.BaseManager import BaseManager
from ext.ModalDialog import SelectFrame

VoiceList = ('jane', 'oksana', 'alyss', 'omazh', 'zahar', 'ermil')


class VoiceManager(BaseManager):
    """description of class"""

    def __init__(self, root):
        """ """
        super(VoiceManager, self).__init__(root, text="Настройки голосового модуля")
        self._speakerValue = StringVar()
        self._keyValue = StringVar()

        lbl = ttk.Label(self, text="Голос")
        lbl.grid(row=0, column=0, padx=2, pady=2)

        combo = ttk.Combobox(self, state="readonly", values=VoiceList, textvariable=self._speakerValue)
        combo.grid(row=0, column=1, padx=2, pady=2)

        lbl = ttk.Label(self, text="Яндекс ключ")
        lbl.grid(row=0, column=2, padx=2, pady=2)

        entr = ttk.Entry(self, textvariable=self._keyValue, width=35)
        entr.grid(row=0, column=3, padx=2, pady=2)

        self._frame = SelectFrame(self, "Выбор модулей")
        self._frame.grid(row=1, column=0, columnspan=4, sticky=(N, S, E, W), padx=2, pady=2)

    def load(self, config, modulelist):
        if not isinstance(config, configparser.ConfigParser):
            raise TypeError("config")
        if not config.has_section("VoiceBlock"):
            config.add_section("VoiceBlock")
        section = config["VoiceBlock"]
        self._speakerValue.set(section.get("Speaker", "omazh"))
        self._keyValue.set(section.get("Key", ""))
        selection = section.get("BlockList", "")
        selection = [item.strip(" '") for item in selection.split(",") if item.strip() in modulelist]
        self._frame.load(selection, modulelist)

    def save(self, config):
        if not isinstance(config, configparser.ConfigParser):
            raise TypeError("config")
        if not config.has_section("VoiceBlock"):
            config.add_section("VoiceBlock")
        section = config["VoiceBlock"]
        section["Speaker"] = self._speakerValue.get()
        section["Key"] = self._keyValue.get()
        section["BlockList"] = self._frame.getResult()
