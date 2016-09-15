import datetime
import configparser

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import colorchooser

from ext.ModalDialog import ColorsChooserFrame

class AlarmTimeSetting(ttk.LabelFrame):
    """description of class"""

    def __init__(self, root, sectionName):
        """ """
        if not isinstance(sectionName, str): raise TypeError("sectionName")
        super(AlarmTimeSetting, self).__init__(root, text="Настройка будильника: {0}".format(sectionName))
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
        self._hourVariable   = IntVar(value=0)
        self._minuteVariable = IntVar(value=0)
        self._secondVariable = IntVar(value=0)
        self._durationVariable = IntVar(value=0)
        self._fileVariable = StringVar(value="")

        weekDayFrame = ttk.LabelFrame(self, text="Дни недели")
        weekDayFrame.grid(row=0, column=0, columnspan=2, sticky=(N,S,E,W))
        ttk.Checkbutton(weekDayFrame, text="ПН", takefocus=True, variable=self._weekDay0).grid(row=0, column=0, padx=2, pady=2)
        ttk.Checkbutton(weekDayFrame, text="ВТ", takefocus=True, variable=self._weekDay1).grid(row=0, column=1, padx=2, pady=2) 
        ttk.Checkbutton(weekDayFrame, text="СР", takefocus=True, variable=self._weekDay2).grid(row=0, column=2, padx=2, pady=2) 
        ttk.Checkbutton(weekDayFrame, text="ЧТ", takefocus=True, variable=self._weekDay3).grid(row=0, column=3, padx=2, pady=2) 
        ttk.Checkbutton(weekDayFrame, text="ПТ", takefocus=True, variable=self._weekDay4).grid(row=0, column=4, padx=2, pady=2) 
        ttk.Checkbutton(weekDayFrame, text="СБ", takefocus=True, variable=self._weekDay5).grid(row=0, column=5, padx=2, pady=2) 
        ttk.Checkbutton(weekDayFrame, text="ВС", takefocus=True, variable=self._weekDay6).grid(row=0, column=6, padx=2, pady=2)

        timeFrame = ttk.LabelFrame(self, text="Время")
        timeFrame.grid(row=1, column=0, sticky=(N,S,E,W))
        timeFrame.columnconfigure(1, weight=1)
        timeFrame.columnconfigure(3, weight=1)
        timeFrame.columnconfigure(4, weight=1)
        ttk.Label(timeFrame, text="Час:", justify=RIGHT).grid(row=0, column=0, pady=2)
        Spinbox(timeFrame, from_=0, to=23, increment=1, width=3, textvariable=self._hourVariable).grid(row=0, column=1, padx=2, pady=2)
        ttk.Label(timeFrame, text="Мин:", justify=RIGHT).grid(row=0, column=2, pady=2)
        Spinbox(timeFrame, from_=0, to=59, increment=1, width=3, textvariable=self._minuteVariable).grid(row=0, column=3, padx=2, pady=2)
        ttk.Label(timeFrame, text="Сек:", justify=RIGHT).grid(row=0, column=4, pady=2)
        Spinbox(timeFrame, from_=0, to=59, increment=1, width=3, textvariable=self._secondVariable).grid(row=0, column=5, padx=2, pady=2)
        durationFrame = ttk.LabelFrame(self, text="Длительность")
        durationFrame.grid(row=1, column=1, sticky=(N,S,E,W))
        Spinbox(durationFrame, from_=5, to=60, increment=1, width=3, textvariable=self._durationVariable).grid(row=0, column=0, padx=2, pady=2)
        ttk.Label(durationFrame, text="секунд").grid(row=0, column=1, pady=2)
        self._colorFrame = ColorsChooserFrame(self, "Цвет")
        self._colorFrame.grid(row=2, column=0, columnspan=2, sticky=(N,S,E,W))

        fileFrame = ttk.LabelFrame(self, text="Файл для проигрывания")
        fileFrame.grid(row=3, column=0, columnspan=2, sticky=(N,S,E,W))
        ttk.Label(fileFrame, text="Файл:").grid(row=0, column=0, pady=2)
        ttk.Entry(fileFrame, width=34, textvariable=self._fileVariable).grid(row=0, column=1, pady=2)
        ttk.Button(fileFrame, text="...", command=self._selectFile, width=3).grid(row=0, column=2, pady=2)


    def load(self, config, sectionName):
        """ """
        if not isinstance(config, configparser.ConfigParser): raise TypeError("config")
        if not isinstance(sectionName, str):                  raise TypeError("sectionName")
        if self._type is None: raise Exception("Type is None")
        self.config(text="Настройка будильника: {0} (Тип {1})".format(sectionName, self._type))

        section = config[sectionName]
        if section is None: raise Exception("Section {0} not found".format(sectionName))

        #self._type = section.getint("Type", self._type)
        date = section.get("Time", "0:00:00")
        date = datetime.datetime.strptime(date, "%H:%M:%S")
        weekDay = self._getTuple(section.get("WeekDay", "(0, 1, 2, 3, 4)"))
        duration = section.getint("Duration", 5)
        if any(day == 0 for day in weekDay): self._weekDay0.set(1)
        if any(day == 1 for day in weekDay): self._weekDay1.set(1)
        if any(day == 2 for day in weekDay): self._weekDay2.set(1)
        if any(day == 3 for day in weekDay): self._weekDay3.set(1)
        if any(day == 4 for day in weekDay): self._weekDay4.set(1)
        if any(day == 5 for day in weekDay): self._weekDay5.set(1)
        if any(day == 6 for day in weekDay): self._weekDay6.set(1)
        self._hourVariable.set(date.hour)
        self._minuteVariable.set(date.minute)
        self._secondVariable.set(date.second)
        self._durationVariable.set(duration)
        backColor = self._getTuple(section.get("BackgroundColor", "(0, 0, 0)"))
        foreColor = self._getTuple(section.get("ForegroundColor", "(255, 255, 255)"))
        self._colorFrame.load(backColor, foreColor)
        self._fileVariable.set(section.get("File", ""))

    def pre_save(self):
        date = datetime.datetime(year=1900, month=1, day=1,
            hour=self._hourVariable.get(),
            minute=self._minuteVariable.get(),
            second=self._secondVariable.get())
        self._time = datetime.datetime.strftime(date, "%H:%M:%S")

    def save(self, config, sectionName):
        """ """
        if not isinstance(config, configparser.ConfigParser): raise TypeError("config")
        if not isinstance(sectionName, str):                  raise TypeError("sectionName")
        if self._type is None: raise Exception("Type is None")

        if config.has_section(sectionName): config.remove_section(sectionName)
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
        section["File"] = self._fileVariable.get()

    def rename(self, sectionName):
        if not isinstance(sectionName, str): raise TypeError("sectionName")
        self.configure(text="Настройка будильника: {0}".format(sectionName))

    def _selectFile(self): 
        fileName = filedialog. Open(self, filetypes = [('*.* all files', '.*')]).show()
        if fileName == '': return
        self._fileVariable.set(fileName)


    def _getTuple(self, value):
        """  Конвертирует строку '0, 0, 0' в кортеж (0, 0, 0) """
        try:
            return tuple(int(item.strip("([ '])")) for item in value.split(",") if item.strip())
        except Exception as ex:
            return None


class AlarmSimpleSetting(AlarmTimeSetting):
    def __init__(self, root, sectionName):
        """ """
        super(AlarmSimpleSetting, self).__init__(root, sectionName)
        self._type = 1



class AlarmBlinkSetting(AlarmTimeSetting):
    def __init__(self, root, sectionName):
        """ """
        super(AlarmBlinkSetting, self).__init__(root, sectionName)
        self._type = 2


class AlarmRiseSetting(AlarmTimeSetting):
    def __init__(self, root, sectionName):
        """ """
        super(AlarmRiseSetting, self).__init__(root, sectionName)
        self._type = 3
