﻿import configparser 
import datetime

TEXT_EXCEPTION_NOT_FOUND = "Ошибка конфигурации! В секции [{0}] пропущен параметр {1}"
TEXT_EXCEPTION_FORMAT = "Ошибка конфигурации! В секции [{0}] не верный формат параметра {1}"

class Setting:

    def __init__(self):
        """Ininitializes a new instanse"""
        self._backgroundColor = None
        self._foregroundColor = None
        self._idleTime = None
        self._timeLine = []         #Набор кортежей (StartTime, TimeBackgroundColor, TimeForegroundColor, IdleTime)
    
    def load(self, fileName):
        # Загружаем настройки
        config = configparser.ConfigParser()
        config.read(fileName, encoding="utf-8")

        section = config["MAIN"]
        self._backgroundColor = self._getTuple(section.get("BackgroundColor"))
        self._foregroundColor = self._getTuple(section.get("ForegroundColor"))
        self._idleTime = section.getint("IdleTime")

        if not self._backgroundColor: raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(section.name, "BackgroundColor"))
        if not self._foregroundColor: raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(section.name, "ForegroundColor"))
        if not self._idleTime:           raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(section.name, "IdleTime"))

        if len(self._backgroundColor) != 3: raise Exception(TEXT_EXCEPTION_FORMAT.format(section.name, "BackgroundColor"))
        if len(self._foregroundColor) != 3: raise Exception(TEXT_EXCEPTION_FORMAT.format(section.name, "ForegroundColor"))

        section = config["TIMELINE"]
        schemas = section.get("sections")
        if schemas:
            schemas = [item.strip(" '") for item in schemas.split(",") if item.strip()]
            for schema in schemas:
                if not config.has_section(schema):
                    raise Exception("Ошибка конфигурации! Нет секции [{0}]".format(schema))
                section = config[schema]
                start = section.get("StartTime")
                if not start:
                    raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(section.name, "StartTime"))
                start = datetime.datetime.strptime(start, "%H:%M:%S")
                BackgroundColor = self._getTuple(section.get("BackgroundColor"))
                ForegroundColor = self._getTuple(section.get("ForegroundColor"))
                idleTime       = section.getint('IdleTime', self._idleTime)
                if not BackgroundColor: BackgroundColor = self._backgroundColor
                if not ForegroundColor: ForegroundColor = self._foregroundColor
                if len(BackgroundColor) != 3: raise Exception(TEXT_EXCEPTION_FORMAT.format(section.name, "BackgroundColor"))
                if len(ForegroundColor) != 3: raise Exception(TEXT_EXCEPTION_FORMAT.format(section.name, "ForegroundColor"))
                entry = (start, BackgroundColor, ForegroundColor, idleTime)
                self._timeLine.append(entry)
        if len(self._timeLine) == 0:
            entry = (datetime.datetime.strptime("00:00:00", "%H:%M:%S"), self._backgroundColor, self._foregroundColor, self._idleTime)
            self._timeLine.append(entry)
        list.sort(self._timeLine, key=lambda entry: entry[0])


    def get_curret_setting(self):
        value = datetime.datetime.today()
        current = self._timeLine[0]
        for line in self._timeLine[1:]:
            if (value.hour < line[0].hour): break
            if (value.minute < line[0].minute): break
            if (value.second < line[0].second): break
            current = line
        return current


    def _getTuple(self, value):
        """  Конвертирует строку '0, 0, 0' в кортеж (0, 0, 0) """
        try:
            return tuple(int(item.strip("([ '])")) for item in value.split(",") if item.strip())
        except:
            return None

