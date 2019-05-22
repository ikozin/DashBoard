from typing import List
from configparser import ConfigParser
from tkinter import StringVar, LabelFrame, Label, N, S, E, W
from tkinter.ttk import Combobox
from ext.alarm.alarm_setting import AlarmSetting


class AlarmSettingExecute(AlarmSetting):

    def __init__(self, root, section_name: str, mod_List: List[str]):
        super(AlarmSettingExecute, self).__init__(root, section_name, mod_List)
        self._type = 4
        self._module_variable = StringVar(value="")
        frame = LabelFrame(self, text="Модуль для запуска")
        frame.grid(row=3, column=0, columnspan=2, sticky=(N, S, E, W))
        lbl = Label(frame, text="Модуль:")
        lbl.grid(row=0, column=0, pady=2)
        combo = Combobox(frame, state="readonly", values=self._mod_list, textvariable=self._module_variable)
        combo.grid(row=0, column=1, padx=2, pady=2, sticky=(N, S, E, W))

    def load(self, config: ConfigParser, section_name: str) -> None:
        super(AlarmSettingExecute, self).load(config, section_name)
        section = config[section_name]
        self._module_variable.set(section.get("Module", fallback=""))

    def save(self, config: ConfigParser, section_name: str) -> None:
        super(AlarmSettingExecute, self).save(config, section_name)
        section = config[section_name]
        section["Module"] = self._module_variable.get()
