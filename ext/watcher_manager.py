from typing import Dict, Tuple
from configparser import ConfigParser
from datetime import datetime
from tkinter import IntVar, StringVar, LabelFrame, Label, Entry, Spinbox, Checkbutton, Button
from tkinter import filedialog, N, S, E, W, RIGHT, LEFT
from tkinter.ttk import Frame
from ext.base_manager import BaseManager


class WatcherManager(BaseManager):
    """description of class"""

    def __init__(self, root: LabelFrame):
        """ """
        super(WatcherManager, self).__init__(root, text="Настройки Watcher")
        self._weekday0 = IntVar(value=0)
        self._weekday1 = IntVar(value=0)
        self._weekday2 = IntVar(value=0)
        self._weekday3 = IntVar(value=0)
        self._weekday4 = IntVar(value=0)
        self._weekday5 = IntVar(value=0)
        self._weekday6 = IntVar(value=0)
        self._hour_start_variable = IntVar(value=0)
        self._minute_start_variable = IntVar(value=0)
        self._second_start_variable = IntVar(value=0)
        self._hour_finish_variable = IntVar(value=0)
        self._minute_finish_variable = IntVar(value=0)
        self._second_finish_variable = IntVar(value=0)
        self._update_value = IntVar()
        self._path_value = StringVar()

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

        time_start_frame = LabelFrame(self, text="Время (Начало)")
        time_start_frame.grid(row=1, column=0, sticky=(N, S, E, W))

        lbl = Label(time_start_frame, text="Час:", justify=RIGHT)
        lbl.grid(row=0, column=0, pady=2)

        spin = Spinbox(time_start_frame, from_=0, to=23, increment=1, width=3, textvariable=self._hour_start_variable)
        spin.grid(row=0, column=1, padx=2, pady=2)

        lbl = Label(time_start_frame, text="Мин:", justify=RIGHT)
        lbl.grid(row=0, column=2, pady=2)

        spin = Spinbox(time_start_frame, from_=0, to=59, increment=1, width=3, textvariable=self._minute_start_variable)
        spin.grid(row=0, column=3, padx=2, pady=2)

        lbl = Label(time_start_frame, text="Сек:", justify=RIGHT)
        lbl.grid(row=0, column=4, pady=2)

        spin = Spinbox(time_start_frame, from_=0, to=59, increment=1, width=3, textvariable=self._second_start_variable)
        spin.grid(row=0, column=5, padx=2, pady=2)

        time_finish_frame = LabelFrame(self, text="Время (Конец)")
        time_finish_frame.grid(row=2, column=0, sticky=(N, S, E, W))

        lbl = Label(time_finish_frame, text="Час:", justify=RIGHT)
        lbl.grid(row=0, column=0, pady=2)

        spin = Spinbox(time_finish_frame, from_=0, to=23, increment=1, width=3, textvariable=self._hour_finish_variable)
        spin.grid(row=0, column=1, padx=2, pady=2)

        lbl = Label(time_finish_frame, text="Мин:", justify=RIGHT)
        lbl.grid(row=0, column=2, pady=2)

        spin = Spinbox(time_finish_frame, from_=0, to=59, increment=1, width=3, textvariable=self._minute_finish_variable)
        spin.grid(row=0, column=3, padx=2, pady=2)

        lbl = Label(time_finish_frame, text="Сек:", justify=RIGHT)
        lbl.grid(row=0, column=4, pady=2)

        spin = Spinbox(time_finish_frame, from_=0, to=59, increment=1, width=3, textvariable=self._second_finish_variable)
        spin.grid(row=0, column=5, padx=2, pady=2)

        content = Frame(self)
        content.grid(row=3, column=0, padx=2, pady=2, sticky=(N, S, E, W))

        lbl = Label(content, justify=RIGHT, text="Время обновления")
        lbl.grid(row=0, column=0, padx=2, pady=2, sticky=(N, S, E))

        spin = Spinbox(content, from_=5, to=60, increment=1, width=5, textvariable=self._update_value)
        spin.grid(row=0, column=1, padx=2, pady=2, sticky=(N, S, E, W))

        lbl = Label(content, justify=LEFT, text="сек.")
        lbl.grid(row=0, column=2, padx=2, pady=2, sticky=(N, S, W))

        file_frame = LabelFrame(self, text="Файл для запуска")
        file_frame.grid(row=4, column=0, padx=2, pady=2, sticky=(N, S, E, W))

        lbl = Label(file_frame, text="Файл:")
        lbl.grid(row=0, column=0, pady=2)

        Entry(file_frame, width=34, textvariable=self._path_value).grid(row=0, column=1, pady=2)

        Button(file_frame, text="...", command=self._select_file, width=3).grid(row=0, column=2, pady=2)

    def load(self, config: ConfigParser, module_list: Dict[str, BaseManager]) -> None:
        if not isinstance(config, ConfigParser):
            raise TypeError("config")
        if not config.has_section("WatcherBlock"):
            config.add_section("WatcherBlock")
        section = config["WatcherBlock"]

        weekday = self._get_tuple(section.get("WeekDay", fallback="(0, 1, 2, 3, 4)"))
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

        date = datetime.strptime(section.get("StartTime", fallback="9:00:00"), "%H:%M:%S")
        self._hour_start_variable.set(date.hour)
        self._minute_start_variable.set(date.minute)
        self._second_start_variable.set(date.second)

        date = datetime.strptime(section.get("FinishTime", fallback="20:00:00"), "%H:%M:%S")
        self._hour_finish_variable.set(date.hour)
        self._minute_finish_variable.set(date.minute)
        self._second_finish_variable.set(date.second)

        self._update_value.set(section.getint("UpdateTime", fallback=1))
        self._path_value.set(section.get("Path", fallback=""))

    def save(self, config: ConfigParser) -> None:
        if not isinstance(config, ConfigParser):
            raise TypeError("config")
        if not config.has_section("WatcherBlock"):
            config.add_section("WatcherBlock")
        section = config["WatcherBlock"]

        var_weekday = (
            self._weekday0.get(),
            self._weekday1.get(),
            self._weekday2.get(),
            self._weekday3.get(),
            self._weekday4.get(),
            self._weekday5.get(),
            self._weekday6.get(),
        )
        weekday = [str(index) for (index, value) in enumerate(var_weekday) if value != 0]
        section["WeekDay"] = ", ".join(weekday)

        date = datetime(
            year=1900,
            month=1,
            day=1,
            hour=self._hour_start_variable.get(),
            minute=self._minute_start_variable.get(),
            second=self._second_start_variable.get())
        section["StartTime"] = datetime.strftime(date, "%H:%M:%S")

        date = datetime(
            year=1900,
            month=1,
            day=1,
            hour=self._hour_finish_variable.get(),
            minute=self._minute_finish_variable.get(),
            second=self._second_finish_variable.get())
        section["FinishTime"] = datetime.strftime(date, "%H:%M:%S")
        section["UpdateTime"] = str(self._update_value.get())
        section["Path"] = self._path_value.get()

    def _select_file(self) -> None:
        file_name = filedialog.Open(self, filetypes=[('*.* all files', '.*')]).show()
        if file_name == '':
            return
        self._path_value.set(file_name)

    def _get_tuple(self, value: str) -> Tuple[int, ...]:
        """  Конвертирует строку '0, 0, 0' в кортеж (0, 0, 0) """
        return tuple(int(item.strip("([ '])")) for item in value.split(",") if item.strip())
