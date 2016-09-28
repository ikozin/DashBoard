import configparser
import datetime

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
        self._weekDay0 = IntVar(value=0)
        self._weekDay1 = IntVar(value=0)
        self._weekDay2 = IntVar(value=0)
        self._weekDay3 = IntVar(value=0)
        self._weekDay4 = IntVar(value=0)
        self._weekDay5 = IntVar(value=0)
        self._weekDay6 = IntVar(value=0)
        self._hourStartVariable   = IntVar(value=0)
        self._minuteStartVariable = IntVar(value=0)
        self._secondStartVariable = IntVar(value=0)
        self._hourFinishVariable   = IntVar(value=0)
        self._minuteFinishVariable = IntVar(value=0)
        self._secondFinishVariable = IntVar(value=0)
        self._updateValue = IntVar()
        self._pathValue = StringVar()

        weekDayFrame = ttk.LabelFrame(self, text="Дни недели")
        weekDayFrame.grid(row=0, column=0, columnspan=2, sticky=(N,S,E,W))
        ttk.Checkbutton(weekDayFrame, text="ПН", takefocus=True, variable=self._weekDay0).grid(row=0, column=0, padx=2, pady=2)
        ttk.Checkbutton(weekDayFrame, text="ВТ", takefocus=True, variable=self._weekDay1).grid(row=0, column=1, padx=2, pady=2) 
        ttk.Checkbutton(weekDayFrame, text="СР", takefocus=True, variable=self._weekDay2).grid(row=0, column=2, padx=2, pady=2) 
        ttk.Checkbutton(weekDayFrame, text="ЧТ", takefocus=True, variable=self._weekDay3).grid(row=0, column=3, padx=2, pady=2) 
        ttk.Checkbutton(weekDayFrame, text="ПТ", takefocus=True, variable=self._weekDay4).grid(row=0, column=4, padx=2, pady=2) 
        ttk.Checkbutton(weekDayFrame, text="СБ", takefocus=True, variable=self._weekDay5).grid(row=0, column=5, padx=2, pady=2) 
        ttk.Checkbutton(weekDayFrame, text="ВС", takefocus=True, variable=self._weekDay6).grid(row=0, column=6, padx=2, pady=2)

        timeStartFrame = ttk.LabelFrame(self, text="Время (Начало)")
        timeStartFrame.grid(row=1, column=0, sticky=(N,S,E,W))
        ttk.Label(timeStartFrame, text="Час:", justify=RIGHT).grid(row=0, column=0, pady=2)
        Spinbox(timeStartFrame, from_=0, to=23, increment=1, width=3, textvariable=self._hourStartVariable).grid(row=0, column=1, padx=2, pady=2)
        ttk.Label(timeStartFrame, text="Мин:", justify=RIGHT).grid(row=0, column=2, pady=2)
        Spinbox(timeStartFrame, from_=0, to=59, increment=1, width=3, textvariable=self._minuteStartVariable).grid(row=0, column=3, padx=2, pady=2)
        ttk.Label(timeStartFrame, text="Сек:", justify=RIGHT).grid(row=0, column=4, pady=2)
        Spinbox(timeStartFrame, from_=0, to=59, increment=1, width=3, textvariable=self._secondStartVariable).grid(row=0, column=5, padx=2, pady=2)

        timeFinishFrame = ttk.LabelFrame(self, text="Время (Конец)")
        timeFinishFrame.grid(row=2, column=0, sticky=(N,S,E,W))
        ttk.Label(timeFinishFrame, text="Час:", justify=RIGHT).grid(row=0, column=0, pady=2)
        Spinbox(timeFinishFrame, from_=0, to=23, increment=1, width=3, textvariable=self._hourFinishVariable).grid(row=0, column=1, padx=2, pady=2)
        ttk.Label(timeFinishFrame, text="Мин:", justify=RIGHT).grid(row=0, column=2, pady=2)
        Spinbox(timeFinishFrame, from_=0, to=59, increment=1, width=3, textvariable=self._minuteFinishVariable).grid(row=0, column=3, padx=2, pady=2)
        ttk.Label(timeFinishFrame, text="Сек:", justify=RIGHT).grid(row=0, column=4, pady=2)
        Spinbox(timeFinishFrame, from_=0, to=59, increment=1, width=3, textvariable=self._secondFinishVariable).grid(row=0, column=5, padx=2, pady=2)

        content = ttk.Frame(self)
        content.grid(row=3, column=0, padx=2, pady=2, sticky=(N,S,E,W))
        ttk.Label(content, justify=RIGHT, text="Время обновления").grid(row=0, column=0, padx=2, pady=2, sticky=(N,S,E))
        Spinbox(content, from_=5, to=60, increment=1, width=5, textvariable=self._updateValue).grid(row=0, column=1, padx=2, pady=2, sticky=(N,S,E,W))
        ttk.Label(content, justify=LEFT, text="сек.").grid(row=0, column=2, padx=2, pady=2, sticky=(N,S,W))

        fileFrame = ttk.LabelFrame(self, text="Файл для запуска")
        fileFrame.grid(row=4, column=0, padx=2, pady=2, sticky=(N,S,E,W))
        ttk.Label(fileFrame, text="Файл:").grid(row=0, column=0, pady=2)
        ttk.Entry(fileFrame, width=34, textvariable=self._pathValue).grid(row=0, column=1, pady=2)
        ttk.Button(fileFrame, text="...", command=self._selectFile, width=3).grid(row=0, column=2, pady=2)


    def load(self, config, modulelist):
        """ """
        if not isinstance(config, configparser.ConfigParser): raise TypeError("config")
        if not config.has_section("WatcherBlock"):      config.add_section("WatcherBlock")
        section = config["WatcherBlock"]

        weekDay = self._getTuple(section.get("WeekDay", "(0, 1, 2, 3, 4)"))
        if any(day == 0 for day in weekDay): self._weekDay0.set(1)
        if any(day == 1 for day in weekDay): self._weekDay1.set(1)
        if any(day == 2 for day in weekDay): self._weekDay2.set(1)
        if any(day == 3 for day in weekDay): self._weekDay3.set(1)
        if any(day == 4 for day in weekDay): self._weekDay4.set(1)
        if any(day == 5 for day in weekDay): self._weekDay5.set(1)
        if any(day == 6 for day in weekDay): self._weekDay6.set(1)

        date = section.get("StartTime", "9:00:00")
        date = datetime.datetime.strptime(date, "%H:%M:%S")
        self._hourStartVariable.set(date.hour)
        self._minuteStartVariable.set(date.minute)
        self._secondStartVariable.set(date.second)

        date = section.get("FinishTime", "20:00:00")
        date = datetime.datetime.strptime(date, "%H:%M:%S")
        self._hourFinishVariable.set(date.hour)
        self._minuteFinishVariable.set(date.minute)
        self._secondFinishVariable.set(date.second)

        self._updateValue.set(section.getint("UpdateTime", 1))
        self._pathValue.set(section.get("Path", ""))


    def save(self, config):
        """ """
        if not isinstance(config, configparser.ConfigParser): raise TypeError("config")
        if not config.has_section("WatcherBlock"):      config.add_section("WatcherBlock")
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

        date = datetime.datetime(year=1900, month=1, day=1,
            hour=self._hourStartVariable.get(),
            minute=self._minuteStartVariable.get(),
            second=self._secondStartVariable.get())
        section["StartTime"] = datetime.datetime.strftime(date, "%H:%M:%S")

        date = datetime.datetime(year=1900, month=1, day=1,
            hour=self._hourFinishVariable.get(),
            minute=self._minuteFinishVariable.get(),
            second=self._secondFinishVariable.get())
        section["FinishTime"] = datetime.datetime.strftime(date, "%H:%M:%S")

        section["UpdateTime"] = str(self._updateValue.get())
        section["Path"] = self._pathValue.get()

    def _selectFile(self): 
        fileName = filedialog. Open(self, filetypes = [('*.* all files', '.*')]).show()
        if fileName == '': return
        self._pathValue.set(fileName)

    def _getTuple(self, value):
        """  Конвертирует строку '0, 0, 0' в кортеж (0, 0, 0) """
        try:
            return tuple(int(item.strip("([ '])")) for item in value.split(",") if item.strip())
        except Exception as ex:
            return None
