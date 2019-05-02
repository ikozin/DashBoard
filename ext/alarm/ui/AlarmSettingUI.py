from typing import *

from datetime import datetime
from configparser import ConfigParser
from tkinter import *
from tkinter import filedialog

from ext.BaseSetting import BaseSetting
from ext.ModalDialog import ColorsChooserFrame
from ext.alarm.AlarmSetting import AlarmSetting


class AlarmSettingUI(AlarmSetting):
    """description of class"""

    def __init__(self, root: LabelFrame, sectionName: str, modList: List[str]):
        """ """
        super(AlarmSettingUI, self).__init__(root, sectionName, modList)
        self._colorFrame = None
        self._durationVariable = IntVar(value=0)
        durationFrame = LabelFrame(self, text="Длительность")
        durationFrame.grid(row=1, column=1, sticky=(N, S, E, W))
        spin = Spinbox(durationFrame, from_=5, to=60, increment=1, width=3, textvariable=self._durationVariable)
        spin.grid(row=0, column=0, padx=2, pady=2)
        lbl = Label(durationFrame, text="секунд")
        lbl.grid(row=0, column=1, pady=2)
        self._colorFrame = ColorsChooserFrame(self, "Цвет")
        self._colorFrame.grid(row=2, column=0, columnspan=2, sticky=(N, S, E, W))

    def load(self, config: ConfigParser, sectionName: str) -> None:
        """ """
        super(AlarmSettingUI, self).load(config, sectionName)
        section = config[sectionName]
        duration = section.getint("Duration", 5)
        self._durationVariable.set(duration)
        backColor = self._getTuple(section.get("BackgroundColor", "(0, 0, 0)"))
        foreColor = self._getTuple(section.get("ForegroundColor", "(255, 255, 255)"))
        self._colorFrame.load(backColor, foreColor)

    def save(self, config: ConfigParser, sectionName: str) -> None:
        """ """
        super(AlarmSettingUI, self).save(config, sectionName)
        section = config[sectionName]
        (backgroundColor, foregroundColor) = self._colorFrame.getResult()
        section["Duration"] = str(self._durationVariable.get())
        section["BackgroundColor"] = "(%d, %d, %d)" % backgroundColor
        section["ForegroundColor"] = "(%d, %d, %d)" % foregroundColor
