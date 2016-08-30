import configparser

from tkinter import *
from tkinter import font
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import colorchooser

class WatcherManager(ttk.LabelFrame):
    """description of class"""

    def __init__(self, root):
        """ """
        super(WatcherManager, self).__init__(root, text="Настройки Watcher")
        self._updateValue = IntVar()
        self._pathValue = StringVar()

        content = ttk.Frame(self)
        content.grid(row=0, column=0, padx=2, pady=2, sticky=(N,S,E,W))
        
        ttk.Label(content, justify=RIGHT, text="Время обновления").grid(row=0, column=0, padx=2, pady=2, sticky=(N,S,E))
        Spinbox(content, from_=1, to=60, increment=1, width=5, textvariable=self._updateValue).grid(row=0, column=1, padx=2, pady=2, sticky=(N,S,E,W))
        ttk.Label(content, justify=LEFT, text="минут").grid(row=0, column=2, padx=2, pady=2, sticky=(N,S,W))

        fileFrame = ttk.LabelFrame(self, text="Файл для запуска")
        fileFrame.grid(row=1, column=0, padx=2, pady=2, sticky=(N,S,E,W))
        ttk.Label(fileFrame, text="Файл:").grid(row=0, column=0, pady=2)
        ttk.Entry(fileFrame, width=34, textvariable=self._pathValue).grid(row=0, column=1, pady=2)
        ttk.Button(fileFrame, text="...", command=self._selectFile, width=3).grid(row=0, column=2, pady=2)


    def load(self, config):
        """ """
        if not isinstance(config, configparser.ConfigParser): raise TypeError("config")
        if not config.has_section("WatcherBlock"):      config.add_section("WatcherBlock")
        section = config["WatcherBlock"]
        self._updateValue.set(section.getint("UpdateTime", 1))
        self._pathValue.set(section.get("Path", ""))

    def save(self, config):
        """ """
        if not isinstance(config, configparser.ConfigParser): raise TypeError("config")
        if not config.has_section("WatcherBlock"):      config.add_section("WatcherBlock")
        section = config["WatcherBlock"]

        section["UpdateTime"] = str(self._updateValue.get())
        section["Path"] = self._pathValue.get()

    def _selectFile(self): 
        fileName = filedialog. Open(self, filetypes = [('*.* all files', '.*')]).show()
        if fileName == '': return
        self._pathValue.set(fileName)
