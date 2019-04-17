import configparser
import datetime
import pygame
import pygame.locals

from exceptions import ExceptionFormat, ExceptionNotFound

BLOCK_SECOND_UPDATE_EVENT = (pygame.locals.USEREVENT + 2)
BLOCK_MINUTE_UPDATE_EVENT = (pygame.locals.USEREVENT + 3)


class Setting:

    def __init__(self):
        """Ininitializes a new instanse"""
        self._config = None
        self._backgroundColor = None
        self._foregroundColor = None
        self._blockList = []
        self._idleTime = None
        self._timeLine = []         # Набор кортежей (StartTime, BackgroundColor, ForegroundColor, IdleTime)

    def load(self, fileName):
        # Загружаем настройки
        self._config = configparser.ConfigParser()
        self._config.read(fileName, encoding="utf-8")

        section = self._config["MAIN"]
        self._backgroundColor = self.getTuple(section.get("BackgroundColor"))
        self._foregroundColor = self.getTuple(section.get("ForegroundColor"))
        self._idleTime = section.getint("IdleTime")
        selection = section.get("BlockList", "")
        self._blockList = [item.strip(" '") for item in selection.split(",") if item.strip()]

        if not self._backgroundColor:
            raise ExceptionNotFound(section.name, "BackgroundColor")
        if not self._foregroundColor:
            raise ExceptionNotFound(section.name, "ForegroundColor")
        if not self._idleTime:
            raise ExceptionNotFound(section.name, "IdleTime")
        if not self._blockList:
            raise ExceptionNotFound(section.name, "BlockList")

        if len(self._backgroundColor) != 3:
            raise ExceptionFormat(section.name, "BackgroundColor")
        if len(self._foregroundColor) != 3:
            raise ExceptionFormat(section.name, "ForegroundColor")

        section = self._config["TIMELINE"]
        schemas = section.get("sections")
        if schemas:
            schemas = [item.strip(" '") for item in schemas.split(",") if item.strip()]
            for schema in schemas:
                if not self._config.has_section(schema):
                    raise Exception("Ошибка конфигурации! Нет секции [{0}]".format(schema))
                section = self._config[schema]
                start = section.get("StartTime")
                if not start:
                    raise ExceptionNotFound(section.name, "StartTime")
                start = datetime.datetime.strptime(start, "%H:%M:%S")
                BackgroundColor = self.getTuple(section.get("BackgroundColor"))
                ForegroundColor = self.getTuple(section.get("ForegroundColor"))
                idleTime = section.getint('IdleTime', self._idleTime)

                if not BackgroundColor:
                    BackgroundColor = self._backgroundColor
                if not ForegroundColor:
                    ForegroundColor = self._foregroundColor
                if len(BackgroundColor) != 3:
                    raise ExceptionFormat(section.name, "BackgroundColor")
                if len(ForegroundColor) != 3:
                    raise ExceptionFormat(section.name, "ForegroundColor")

                entry = (start, BackgroundColor, ForegroundColor, idleTime)
                self._timeLine.append(entry)
        if len(self._timeLine) == 0:
            entry = (
                datetime.datetime.strptime("00:00:00", "%H:%M:%S"),
                self._backgroundColor,
                self._foregroundColor,
                self._idleTime)
            self._timeLine.append(entry)
        list.sort(self._timeLine, key=lambda entry: entry[0])

    def get_curret_setting(self):
        value = datetime.datetime.today()
        current = self._timeLine[0]
        for line in self._timeLine[1:]:
            if (value.hour < line[0].hour):
                break
            if (value.minute < line[0].minute):
                break
            if (value.second < line[0].second):
                break
            current = line
        return current

    def getTuple(self, value, logger=None):
        """  Конвертирует строку '0, 0, 0' в кортеж (0, 0, 0) """
        try:
            return tuple(int(item.strip("([ '])")) for item in value.split(",") if item.strip())
        except Exception as ex:
            if logger:
                logger.exception(ex)
            return None
