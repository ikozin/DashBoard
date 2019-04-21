from typing import *

from datetime import datetime
from configparser import ConfigParser
from tkinter import *
from tkinter import filedialog

from ext.BaseSetting import BaseSetting
from ext.ModalDialog import ColorsChooserFrame


class AlarmSettingTime(BaseSetting):
    """description of class"""

    def __init__(self, root: LabelFrame, sectionName: str):
        """ """
        if not isinstance(sectionName, str):
            raise TypeError("sectionName")
        super(AlarmSettingTime, self).__init__(root, text="Настройка будильника: {0}".format(sectionName))
        self.columnconfigure(9, weight=1)
        self._type = None
        self._colorFrame = None
        self._time = None
        self._weekDay0 = IntVar(value=0)
        self._weekDay1 = IntVar(value=0)
        self._weekDay2 = IntVar(value=0)
        self._weekDay3 = IntVar(value=0)
        self._weekDay4 = IntVar(value=0)
        self._weekDay5 = IntVar(value=0)
        self._weekDay6 = IntVar(value=0)
        self._hourVariable = IntVar(value=0)
        self._minuteVariable = IntVar(value=0)
        self._secondVariable = IntVar(value=0)
        self._durationVariable = IntVar(value=0)

        weekDayFrame = LabelFrame(self, text="Дни недели")
        weekDayFrame.grid(row=0, column=0, columnspan=2, sticky=(N, S, E, W))

        chk = Checkbutton(weekDayFrame, text="ПН", takefocus=True, variable=self._weekDay0)
        chk.grid(row=0, column=0, padx=2, pady=2)
        chk = Checkbutton(weekDayFrame, text="ВТ", takefocus=True, variable=self._weekDay1)
        chk.grid(row=0, column=1, padx=2, pady=2)
        chk = Checkbutton(weekDayFrame, text="СР", takefocus=True, variable=self._weekDay2)
        chk.grid(row=0, column=2, padx=2, pady=2)
        chk = Checkbutton(weekDayFrame, text="ЧТ", takefocus=True, variable=self._weekDay3)
        chk.grid(row=0, column=3, padx=2, pady=2)
        chk = Checkbutton(weekDayFrame, text="ПТ", takefocus=True, variable=self._weekDay4)
        chk.grid(row=0, column=4, padx=2, pady=2)
        chk = Checkbutton(weekDayFrame, text="СБ", takefocus=True, variable=self._weekDay5)
        chk.grid(row=0, column=5, padx=2, pady=2)
        chk = Checkbutton(weekDayFrame, text="ВС", takefocus=True, variable=self._weekDay6)
        chk.grid(row=0, column=6, padx=2, pady=2)

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
        if not isinstance(config, ConfigParser):
            raise TypeError("config")
        if not isinstance(sectionName, str):
            raise TypeError("sectionName")
        if self._type is None:
            raise Exception("Type is None")
        self.config(text="Настройка будильника: {0} (Тип {1})".format(sectionName, self._type))

        section = config[sectionName]
        if section is None:
            raise Exception("Section {0} not found".format(sectionName))

        # self._type = section.getint("Type", self._type)
        date = section.get("Time", "0:00:00")
        date = datetime.strptime(date, "%H:%M:%S")
        weekDay = self._getTuple(section.get("WeekDay", "(0, 1, 2, 3, 4)"))
        duration = section.getint("Duration", 5)
        if any(day == 0 for day in weekDay):
            self._weekDay0.set(1)
        if any(day == 1 for day in weekDay):
            self._weekDay1.set(1)
        if any(day == 2 for day in weekDay):
            self._weekDay2.set(1)
        if any(day == 3 for day in weekDay):
            self._weekDay3.set(1)
        if any(day == 4 for day in weekDay):
            self._weekDay4.set(1)
        if any(day == 5 for day in weekDay):
            self._weekDay5.set(1)
        if any(day == 6 for day in weekDay):
            self._weekDay6.set(1)
        self._hourVariable.set(date.hour)
        self._minuteVariable.set(date.minute)
        self._secondVariable.set(date.second)
        self._durationVariable.set(duration)
        backColor = self._getTuple(section.get("BackgroundColor", "(0, 0, 0)"))
        foreColor = self._getTuple(section.get("ForegroundColor", "(255, 255, 255)"))
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
        if self._type is None:
            raise Exception("Type is None")

        if config.has_section(sectionName):
            config.remove_section(sectionName)
        config.add_section(sectionName)
        section = config[sectionName]
        weekday = (
                    self._weekDay0.get(),
                    self._weekDay1.get(),
                    self._weekDay2.get(),
                    self._weekDay3.get(),
                    self._weekDay4.get(),
                    self._weekDay5.get(),
                    self._weekDay6.get(),
                  )
        weekday = [str(index) for (index, value) in enumerate(weekday) if value != 0]
        (backgroundColor, foregroundColor) = self._colorFrame.getResult()
        section["Type"] = str(self._type)
        section["Time"] = self._time
        section["WeekDay"] = ", ".join(weekday)
        section["Duration"] = str(self._durationVariable.get())
        section["BackgroundColor"] = "(%d, %d, %d)" % backgroundColor
        section["ForegroundColor"] = "(%d, %d, %d)" % foregroundColor

    def rename(self, sectionName: str) -> None:
        if not isinstance(sectionName, str):
            raise TypeError("sectionName")
        self.configure(text="Настройка будильника: {0}".format(sectionName))

    def _getTuple(self, value: str) -> Tuple[int, int, int]:
        """  Конвертирует строку '0, 0, 0' в кортеж (0, 0, 0) """
        try:
            return tuple(int(item.strip("([ '])")) for item in value.split(",") if item.strip())
        except Exception as ex:
            return None
