from typing import *

from configparser import ConfigParser
from datetime import datetime
from tkinter import *

from ext.BaseManager import BaseManager


class WatcherManager(BaseManager):
    """description of class"""

    def __init__(self, root: LabelFrame):
        """ """
        super(WatcherManager, self).__init__(root, text="Настройки Watcher")
        self._weekDay0 = IntVar(value=0)
        self._weekDay1 = IntVar(value=0)
        self._weekDay2 = IntVar(value=0)
        self._weekDay3 = IntVar(value=0)
        self._weekDay4 = IntVar(value=0)
        self._weekDay5 = IntVar(value=0)
        self._weekDay6 = IntVar(value=0)
        self._hourStartVariable = IntVar(value=0)
        self._minuteStartVariable = IntVar(value=0)
        self._secondStartVariable = IntVar(value=0)
        self._hourFinishVariable = IntVar(value=0)
        self._minuteFinishVariable = IntVar(value=0)
        self._secondFinishVariable = IntVar(value=0)
        self._updateValue = IntVar()
        self._pathValue = StringVar()

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

        timeStartFrame = LabelFrame(self, text="Время (Начало)")
        timeStartFrame.grid(row=1, column=0, sticky=(N, S, E, W))

        lbl = Label(timeStartFrame, text="Час:", justify=RIGHT)
        lbl.grid(row=0, column=0, pady=2)

        spin = Spinbox(timeStartFrame, from_=0, to=23, increment=1, width=3, textvariable=self._hourStartVariable)
        spin.grid(row=0, column=1, padx=2, pady=2)

        lbl = Label(timeStartFrame, text="Мин:", justify=RIGHT)
        lbl.grid(row=0, column=2, pady=2)

        spin = Spinbox(timeStartFrame, from_=0, to=59, increment=1, width=3, textvariable=self._minuteStartVariable)
        spin.grid(row=0, column=3, padx=2, pady=2)

        lbl = Label(timeStartFrame, text="Сек:", justify=RIGHT)
        lbl.grid(row=0, column=4, pady=2)

        spin = Spinbox(timeStartFrame, from_=0, to=59, increment=1, width=3, textvariable=self._secondStartVariable)
        spin.grid(row=0, column=5, padx=2, pady=2)

        timeFinishFrame = LabelFrame(self, text="Время (Конец)")
        timeFinishFrame.grid(row=2, column=0, sticky=(N, S, E, W))

        lbl = Label(timeFinishFrame, text="Час:", justify=RIGHT)
        lbl.grid(row=0, column=0, pady=2)

        spin = Spinbox(timeFinishFrame, from_=0, to=23, increment=1, width=3, textvariable=self._hourFinishVariable)
        spin.grid(row=0, column=1, padx=2, pady=2)

        lbl = Label(timeFinishFrame, text="Мин:", justify=RIGHT)
        lbl.grid(row=0, column=2, pady=2)

        spin = Spinbox(timeFinishFrame, from_=0, to=59, increment=1, width=3, textvariable=self._minuteFinishVariable)
        spin.grid(row=0, column=3, padx=2, pady=2)

        lbl = Label(timeFinishFrame, text="Сек:", justify=RIGHT)
        lbl.grid(row=0, column=4, pady=2)

        spin = Spinbox(timeFinishFrame, from_=0, to=59, increment=1, width=3, textvariable=self._secondFinishVariable)
        spin.grid(row=0, column=5, padx=2, pady=2)

        content = Frame(self)
        content.grid(row=3, column=0, padx=2, pady=2, sticky=(N, S, E, W))

        lbl = Label(content, justify=RIGHT, text="Время обновления")
        lbl.grid(row=0, column=0, padx=2, pady=2, sticky=(N, S, E))

        spin = Spinbox(content, from_=5, to=60, increment=1, width=5, textvariable=self._updateValue)
        spin.grid(row=0, column=1, padx=2, pady=2, sticky=(N, S, E, W))

        lbl = Label(content, justify=LEFT, text="сек.")
        lbl.grid(row=0, column=2, padx=2, pady=2, sticky=(N, S, W))

        fileFrame = LabelFrame(self, text="Файл для запуска")
        fileFrame.grid(row=4, column=0, padx=2, pady=2, sticky=(N, S, E, W))

        lbl = Label(fileFrame, text="Файл:")
        lbl.grid(row=0, column=0, pady=2)

        Entry(fileFrame, width=34, textvariable=self._pathValue).grid(row=0, column=1, pady=2)

        Button(fileFrame, text="...", command=self._selectFile, width=3).grid(row=0, column=2, pady=2)

    def load(self, config: ConfigParser, modulelist: Dict[str, BaseManager]) -> None:
        """ """
        if not isinstance(config, ConfigParser):
            raise TypeError("config")
        if not config.has_section("WatcherBlock"):
            config.add_section("WatcherBlock")
        section = config["WatcherBlock"]

        weekDay = self._getTuple(section.get("WeekDay", "(0, 1, 2, 3, 4)"))
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

        date = section.get("StartTime", "9:00:00")
        date = datetime.strptime(date, "%H:%M:%S")
        self._hourStartVariable.set(date.hour)
        self._minuteStartVariable.set(date.minute)
        self._secondStartVariable.set(date.second)

        date = section.get("FinishTime", "20:00:00")
        date = datetime.strptime(date, "%H:%M:%S")
        self._hourFinishVariable.set(date.hour)
        self._minuteFinishVariable.set(date.minute)
        self._secondFinishVariable.set(date.second)

        self._updateValue.set(section.getint("UpdateTime", 1))
        self._pathValue.set(section.get("Path", ""))

    def save(self, config: ConfigParser) -> None:
        """ """
        if not isinstance(config, ConfigParser):
            raise TypeError("config")
        if not config.has_section("WatcherBlock"):
            config.add_section("WatcherBlock")
        section = config["WatcherBlock"]

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
        section["WeekDay"] = ", ".join(weekday)

        date = datetime(
            year=1900,
            month=1,
            day=1,
            hour=self._hourStartVariable.get(),
            minute=self._minuteStartVariable.get(),
            second=self._secondStartVariable.get())
        section["StartTime"] = datetime.strftime(date, "%H:%M:%S")

        date = datetime(
            year=1900,
            month=1,
            day=1,
            hour=self._hourFinishVariable.get(),
            minute=self._minuteFinishVariable.get(),
            second=self._secondFinishVariable.get())
        section["FinishTime"] = datetime.strftime(date, "%H:%M:%S")

        section["UpdateTime"] = str(self._updateValue.get())
        section["Path"] = self._pathValue.get()

    def _selectFile(self) -> None:
        fileName = filedialog.Open(self, filetypes=[('*.* all files', '.*')]).show()
        if fileName == '':
            return
        self._pathValue.set(fileName)

    def _getTuple(self, value: str) -> Tuple[int, int, int]:
        """  Конвертирует строку '0, 0, 0' в кортеж (0, 0, 0) """
        try:
            return tuple(int(item.strip("([ '])")) for item in value.split(",") if item.strip())
        except Exception as ex:
            return None
