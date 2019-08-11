from typing import List, Tuple
from datetime import datetime
from configparser import ConfigParser
from tkinter import IntVar, LabelFrame, Label, Checkbutton, Spinbox, N, S, E, W, RIGHT
from ext.base_setting import BaseSetting


class AlarmSetting(BaseSetting):
    """description of class"""

    def __init__(self, root: LabelFrame, section_name: str, mod_List: List[str]):
        if not isinstance(section_name, str):
            raise TypeError("section_name")
        super(AlarmSetting, self).__init__(root, text="Настройка будильника: {0}".format(section_name))
        self._mod_list = mod_List
        self.columnconfigure(9, weight=1)
        self._type = -1
        self._time = ""
        self._weekday0 = IntVar(value=0)
        self._weekday1 = IntVar(value=0)
        self._weekday2 = IntVar(value=0)
        self._weekday3 = IntVar(value=0)
        self._weekday4 = IntVar(value=0)
        self._weekday5 = IntVar(value=0)
        self._weekday6 = IntVar(value=0)
        self._hour_variable = IntVar(value=0)
        self._minute_variable = IntVar(value=0)
        self._second_variable = IntVar(value=0)
        self._duration_variable = IntVar(value=0)
        weekday_frame = LabelFrame(self, text="Дни недели")
        weekday_frame.grid(row=0, column=0, columnspan=2, sticky=(N, S, E, W))
        chk = Checkbutton(weekday_frame, text="ПН", takefocus=True, variable=self._weekday0)
        chk.grid(row=0, column=0, padx=2, pady=2)
        chk = Checkbutton(weekday_frame, text="ВТ", takefocus=True, variable=self._weekday1)
        chk.grid(row=0, column=1, padx=2, pady=2)
        chk = Checkbutton(weekday_frame, text="СР", takefocus=True, variable=self._weekday2)
        chk.grid(row=0, column=2, padx=2, pady=2)
        chk = Checkbutton(weekday_frame, text="ЧТ", takefocus=True, variable=self._weekday3)
        chk.grid(row=0, column=3, padx=2, pady=2)
        chk = Checkbutton(weekday_frame, text="ПТ", takefocus=True, variable=self._weekday4)
        chk.grid(row=0, column=4, padx=2, pady=2)
        chk = Checkbutton(weekday_frame, text="СБ", takefocus=True, variable=self._weekday5)
        chk.grid(row=0, column=5, padx=2, pady=2)
        chk = Checkbutton(weekday_frame, text="ВС", takefocus=True, variable=self._weekday6)
        chk.grid(row=0, column=6, padx=2, pady=2)
        time_frame = LabelFrame(self, text="Время")
        time_frame.grid(row=1, column=0, sticky=(N, S, E, W))
        time_frame.columnconfigure(1, weight=1)
        time_frame.columnconfigure(3, weight=1)
        time_frame.columnconfigure(4, weight=1)
        lbl = Label(time_frame, text="Час:", justify=RIGHT)
        lbl.grid(row=0, column=0, pady=2)
        spin = Spinbox(time_frame, from_=0, to=23, increment=1, width=3, textvariable=self._hour_variable)
        spin.grid(row=0, column=1, padx=2, pady=2)
        lbl = Label(time_frame, text="Мин:", justify=RIGHT)
        lbl.grid(row=0, column=2, pady=2)
        spin = Spinbox(time_frame, from_=0, to=59, increment=1, width=3, textvariable=self._minute_variable)
        spin.grid(row=0, column=3, padx=2, pady=2)
        lbl = Label(time_frame, text="Сек:", justify=RIGHT)
        lbl.grid(row=0, column=4, pady=2)
        spin = Spinbox(time_frame, from_=0, to=59, increment=1, width=3, textvariable=self._second_variable)
        spin.grid(row=0, column=5, padx=2, pady=2)
        duration_frame = LabelFrame(self, text="Длительность")
        duration_frame.grid(row=1, column=1, sticky=(N, S, E, W))
        spin = Spinbox(duration_frame, from_=5, to=60, increment=1, width=3, textvariable=self._duration_variable)
        spin.grid(row=0, column=0, padx=2, pady=2)
        lbl = Label(duration_frame, text="секунд")
        lbl.grid(row=0, column=1, pady=2)

    def load(self, config: ConfigParser, section_name: str) -> None:
        if not isinstance(config, ConfigParser):
            raise TypeError("config")
        if not isinstance(section_name, str):
            raise TypeError("section_name")
        if self._type is None:
            raise Exception("Type is None")
        self.config(text="Настройка будильника: {0} (Тип {1})".format(section_name, self._type))
        section = config[section_name]
        if section is None:
            raise Exception("Section {0} not found".format(section_name))
        # self._type = section.getint("Type", fallback=self._type)
        date = datetime.strptime(section.get("Time", fallback="0:00:00"), "%H:%M:%S")
        weekday = self._get_tuple(section.get("weekday", fallback="(0, 1, 2, 3, 4)"))
        if any(day == 0 for day in weekday):
            self._weekday0.set(1)
        if any(day == 1 for day in weekday):
            self._weekday1.set(1)
        if any(day == 2 for day in weekday):
            self._weekday2.set(1)
        if any(day == 3 for day in weekday):
            self._weekday3.set(1)
        if any(day == 4 for day in weekday):
            self._weekday4.set(1)
        if any(day == 5 for day in weekday):
            self._weekday5.set(1)
        if any(day == 6 for day in weekday):
            self._weekday6.set(1)
        self._hour_variable.set(date.hour)
        self._minute_variable.set(date.minute)
        self._second_variable.set(date.second)
        duration = section.getint("Duration", fallback=5)
        self._duration_variable.set(duration)

    def pre_save(self) -> None:
        date = datetime(
            year=1900,
            month=1,
            day=1,
            hour=self._hour_variable.get(),
            minute=self._minute_variable.get(),
            second=self._second_variable.get())
        self._time = datetime.strftime(date, "%H:%M:%S")

    def save(self, config: ConfigParser, section_name: str) -> None:
        if not isinstance(config, ConfigParser):
            raise TypeError("config")
        if not isinstance(section_name, str):
            raise TypeError("section_name")
        if self._type is None:
            raise Exception("Type is None")
        if config.has_section(section_name):
            config.remove_section(section_name)
        config.add_section(section_name)
        section = config[section_name]
        weekday_var = (
            self._weekday0.get(),
            self._weekday1.get(),
            self._weekday2.get(),
            self._weekday3.get(),
            self._weekday4.get(),
            self._weekday5.get(),
            self._weekday6.get(),
        )
        weekday = [str(index) for (index, value) in enumerate(weekday_var) if value != 0]
        section["Type"] = str(self._type)
        section["Time"] = self._time
        section["weekday"] = ", ".join(weekday)
        section["Duration"] = str(self._duration_variable.get())

    def rename(self, section_name: str) -> None:
        if not isinstance(section_name, str):
            raise TypeError("section_name")
        self.configure(text="Настройка будильника: {0}".format(section_name))

    def _get_tuple(self, value: str) -> Tuple[int, ...]:
        """  Конвертирует строку '0, 0, 0' в кортеж (0, 0, 0) """
        return tuple(int(item.strip("([ '])")) for item in value.split(",") if item.strip())
