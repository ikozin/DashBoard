from typing import Tuple
from datetime import datetime
from configparser import ConfigParser
from tkinter import IntVar, LabelFrame, Label, Spinbox, N, S, E, W, RIGHT
from ext.base_setting import BaseSetting
from ext.modal_dialog import ColorsChooserFrame


class MainSetting(BaseSetting):
    """description of class"""

    def __init__(self, root: LabelFrame, section_name: str):
        """ """
        if not isinstance(section_name, str):
            raise TypeError("section_name")
        super(MainSetting, self).__init__(root, text="Настройка расписания: {0}".format(section_name))
        self.columnconfigure(9, weight=1)

        self._time = ""
        self._hour_variable = IntVar(value=0)
        self._minute_variable = IntVar(value=0)
        self._second_variable = IntVar(value=0)
        self._idle_variable = IntVar(value=0)

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

        idle_frame = LabelFrame(self, text="Время простоя")
        idle_frame.grid(row=1, column=1, sticky=(N, S, E, W))

        spin = Spinbox(idle_frame, from_=1, to=60, increment=1, width=3, textvariable=self._idle_variable)
        spin.grid(row=0, column=0, padx=2, pady=2)

        lbl = Label(idle_frame, text="минут")
        lbl.grid(row=0, column=1, pady=2)

        self._color_frame = ColorsChooserFrame(self, "Цвет")
        self._color_frame.grid(row=2, column=0, columnspan=2, sticky=(N, S, E, W))

    def load(self, config: ConfigParser, section_name: str) -> None:
        """ Загрузка данных секции """
        if not isinstance(config, ConfigParser):
            raise TypeError("config")
        if not isinstance(section_name, str):
            raise TypeError("section_name")

        section = config[section_name]
        if section is None:
            raise Exception("Section {0} not found".format(section_name))

        date = datetime.strptime(section.get("StartTime", fallback="0:00:00"), "%H:%M:%S")
        idle = section.getint("IdleTime", fallback=1)

        self._hour_variable.set(date.hour)
        self._minute_variable.set(date.minute)
        self._second_variable.set(date.second)
        self._idle_variable.set(idle)

        back_color = self._get_tuple(section.get("BackgroundColor", fallback="(0, 0, 0)"))
        fore_color = self._get_tuple(section.get("ForegroundColor", fallback="(255, 255, 255)"))
        self._color_frame.load(back_color, fore_color)

    def pre_save(self) -> None:
        """ Подготовка к записи данных секции """
        date = datetime(
            year=1900,
            month=1,
            day=1,
            hour=self._hour_variable.get(),
            minute=self._minute_variable.get(),
            second=self._second_variable.get())
        self._time = datetime.strftime(date, "%H:%M:%S")

    def save(self, config: ConfigParser, section_name: str) -> None:
        """ Запись данных секции """
        if not isinstance(config, ConfigParser):
            raise TypeError("config")
        if not isinstance(section_name, str):
            raise TypeError("section_name")

        if config.has_section(section_name):
            config.remove_section(section_name)
        config.add_section(section_name)
        section = config[section_name]
        (background_color, foreground_color) = self._color_frame.get_result()
        section["StartTime"] = self._time
        section["IdleTime"] = str(self._idle_variable.get())
        section["BackgroundColor"] = "(%d, %d, %d)" % background_color
        section["ForegroundColor"] = "(%d, %d, %d)" % foreground_color

    def rename(self, section_name: str) -> None:
        """ Переименование секции """
        if not isinstance(section_name, str):
            raise TypeError("section_name")
        self.configure(text="Настройка расписания: {0}".format(section_name))

    def _get_tuple(self, value: str) -> Tuple[int, ...]:
        """  Конвертирует строку '0, 0, 0' в кортеж (0, 0, 0) """
        return tuple(int(item.strip("([ '])")) for item in value.split(",") if item.strip())
