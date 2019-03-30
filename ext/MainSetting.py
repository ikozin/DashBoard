from typing import *

from datetime import datetime
from configparser import ConfigParser
from tkinter import *

from ext.BaseSetting import BaseSetting
from ext.ModalDialog import ColorsChooserFrame


class MainSetting(BaseSetting):
    """description of class"""

    def __init__(self, root: LabelFrame, sectionName: str):
        """ """
        if not isinstance(sectionName, str):
            raise TypeError("sectionName")
        super(MainSetting, self).__init__(root, text="Настройка расписания: {0}".format(sectionName))
        self.columnconfigure(9, weight=1)
        self._colorFrame = None

        self._time = None
        self._hourVariable = IntVar(0)
        self._minuteVariable = IntVar(0)
        self._secondVariable = IntVar(0)
        self._idleVariable = IntVar(0)

        timeFrame = LabelFrame(self, text="Время")
        timeFrame.grid(row=1, column=0, sticky=(N, S, E, W))
        timeFrame.columnconfigure(1, weight=1)
        timeFrame.columnconfigure(3, weight=1)
        timeFrame.columnconfigure(4, weight=1)

        lbl = Label(timeFrame, text="Час:", justify=RIGHT)
        lbl.grid(row=0, column=0, pady=2)

        spin = Spinbox(timeFrame, from_=0, to=23, increment=1, width=3, textvariable=self._hourVariable)
        spin.grid(row=0, column=1, padx=2, pady=2)

        lbl = Label(timeFrame, text="Мин:", justify=RIGHT)
        lbl.grid(row=0, column=2, pady=2)

        spin = Spinbox(timeFrame, from_=0, to=59, increment=1, width=3, textvariable=self._minuteVariable)
        spin.grid(row=0, column=3, padx=2, pady=2)

        lbl = Label(timeFrame, text="Сек:", justify=RIGHT)
        lbl.grid(row=0, column=4, pady=2)

        spin = Spinbox(timeFrame, from_=0, to=59, increment=1, width=3, textvariable=self._secondVariable)
        spin.grid(row=0, column=5, padx=2, pady=2)

        idleFrame = LabelFrame(self, text="Время простоя")
        idleFrame.grid(row=1, column=1, sticky=(N, S, E, W))

        spin = Spinbox(idleFrame, from_=1, to=60, increment=1, width=3, textvariable=self._idleVariable)
        spin.grid(row=0, column=0, padx=2, pady=2)

        lbl = Label(idleFrame, text="минут")
        lbl.grid(row=0, column=1, pady=2)

        self._colorFrame = ColorsChooserFrame(self, "Цвет")
        self._colorFrame.grid(row=2, column=0, columnspan=2, sticky=(N, S, E, W))

    def load(self, config: ConfigParser, sectionName: str) -> None:
        """ """
        if not isinstance(config, ConfigParser):
            raise TypeError("config")
        if not isinstance(sectionName, str):
            raise TypeError("sectionName")

        section = config[sectionName]
        if section is None:
            raise Exception("Section {0} not found".format(sectionName))

        date = section.get("starttime", "0:00:00")
        date = datetime.strptime(date, "%H:%M:%S")
        idle = section.getint("idletime", 1)

        self._hourVariable.set(date.hour)
        self._minuteVariable.set(date.minute)
        self._secondVariable.set(date.second)
        self._idleVariable.set(idle)

        backColor = self._getTuple(section.get("backgroundcolor", "(0, 0, 0)"))
        foreColor = self._getTuple(section.get("foregroundcolor", "(255, 255, 255)"))
        self._colorFrame.load(backColor, foreColor)

    def pre_save(self) -> None:
        date = datetime(
            year=1900,
            month=1,
            day=1,
            hour=self._hourVariable.get(),
            minute=self._minuteVariable.get(),
            second=self._secondVariable.get())
        self._time = datetime.strftime(date, "%H:%M:%S")

    def save(self, config: ConfigParser, sectionName: str) -> None:
        """ """
        if not isinstance(config, ConfigParser):
            raise TypeError("config")
        if not isinstance(sectionName, str):
            raise TypeError("sectionName")

        if config.has_section(sectionName):
            config.remove_section(sectionName)
        config.add_section(sectionName)
        section = config[sectionName]
        (backgroundColor, foregroundColor) = self._colorFrame.getResult()
        section["starttime"] = self._time
        section["idletime"] = str(self._idleVariable.get())
        section["backgroundcolor"] = "(%d, %d, %d)" % backgroundColor
        section["foregroundcolor"] = "(%d, %d, %d)" % foregroundColor

    def rename(self, sectionName: str) -> None:
        if not isinstance(sectionName, str):
            raise TypeError("sectionName")
        self.configure(text="Настройка расписания: {0}".format(sectionName))

    def _getTuple(self, value: str) -> Tuple[int, int, int]:
        """  Конвертирует строку '0, 0, 0' в кортеж (0, 0, 0) """
        try:
            return tuple(int(item.strip("([ '])")) for item in value.split(",") if item.strip())
        except Exception as ex:
            return None
