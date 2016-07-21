import configparser

from tkinter import *
from tkinter import font
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import colorchooser

class VoiceManager(ttk.LabelFrame):
    """description of class"""

    def __init__(self, root):
        """ """
        super(VoiceManager, self).__init__(root, text="Настройки голосового модуля")
        self._speakerValue = StringVar()
        self._keyValue = StringVar()
        ttk.Label(self, text="Голос").grid(row=0, column=0, padx=2, pady=2)
        ttk.Combobox(self, state="readonly", values=('jane', 'oksana', 'alyss', 'omazh', 'zahar', 'ermil'), textvariable=self._speakerValue).grid(row=0, column=1, padx=2, pady=2)
        ttk.Label(self, text="Яндекс ключ").grid(row=0, column=2, padx=2, pady=2)
        ttk.Entry(self, textvariable=self._keyValue, width=40).grid(row=0, column=3, padx=2, pady=2)
        

    def load(self, config):
        if not isinstance(config, configparser.ConfigParser): raise TypeError("config")
        section = config["VoiceBlock"]
        self._speakerValue.set(section.get("Speaker", "omazh"))
        self._keyValue.set(section.get("Key", ""))

    def save(self, config):
        if not isinstance(config, configparser.ConfigParser): raise TypeError("config")
        if not config.has_section("VoiceBlock"):      config.add_section("VoiceBlock")
        section = config["VoiceBlock"]
        section["Speaker"] = self._speakerValue.get()
        section["Key"] = self._keyValue.get()

