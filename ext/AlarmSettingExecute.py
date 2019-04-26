from typing import *

from configparser import ConfigParser
from tkinter import *

from ext.AlarmSettingTime import AlarmSettingTime


class AlarmSettingExecute(AlarmSettingTime):
    def __init__(self, root, sectionName: str, modList: List[str]):
        """ """
        super(AlarmSettingExecute, self).__init__(root, sectionName, modList)
        self._type = 4

        self._moduleVariable = StringVar(value="")

        frame = LabelFrame(self, text="Модуль для запуска")
        frame.grid(row=3, column=0, columnspan=2, sticky=(N, S, E, W))

        lbl = Label(frame, text="Модуль:")
        lbl.grid(row=0, column=0, pady=2)

        combo = ttk.Combobox(frame, state="readonly", values=self._modList, textvariable=self._moduleVariable)
        combo.grid(row=0, column=1, padx=2, pady=2, sticky=(N, S, E, W))

    def load(self, config: ConfigParser, sectionName: str) -> None:
        """ """
        super(AlarmSettingExecute, self).load(config, sectionName)
        section = config[sectionName]
        self._moduleVariable.set(section.get("Module", ""))

    def save(self, config: ConfigParser, sectionName: str) -> None:
        """ """
        super(AlarmSettingExecute, self).save(config, sectionName)
        section = config[sectionName]
        section["Module"] = self._moduleVariable.get()
