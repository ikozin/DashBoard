import configparser
import datetime
from exceptions import ExceptionFormat, ExceptionNotFound
import pygame
import pygame.locals

BLOCK_SECOND_UPDATE_EVENT = (pygame.locals.USEREVENT + 2)
BLOCK_MINUTE_UPDATE_EVENT = (pygame.locals.USEREVENT + 3)


class Setting:

    def __init__(self):
        """Ininitializes a new instanse"""
        self._config = configparser.ConfigParser(interpolation=None)
        self._background_color = None
        self._foreground_color = None
        self._block_list = []
        self._idle_time = None
        self._time_line = []         # Набор кортежей (StartTime, background_color, foreground_color, IdleTime)

    def load(self, file_name):
        # Загружаем настройки
        self._config.read(file_name, encoding="utf-8")

        section = self._config["MAIN"]
        self._background_color = self.get_tuple(section.get("BackgroundColor"))
        self._foreground_color = self.get_tuple(section.get("ForegroundColor"))
        self._idle_time = section.getint("IdleTime")
        selection = section.get("BlockList", fallback="")
        self._block_list = [item.strip(" '") for item in selection.split(",") if item.strip()]

        if not self._background_color:
            raise ExceptionNotFound(section.name, "BackgroundColor")
        if not self._foreground_color:
            raise ExceptionNotFound(section.name, "ForegroundColor")
        if not self._idle_time:
            raise ExceptionNotFound(section.name, "IdleTime")
        if not self._block_list:
            raise ExceptionNotFound(section.name, "BlockList")

        if len(self._background_color) != 3:
            raise ExceptionFormat(section.name, "BackgroundColor")
        if len(self._foreground_color) != 3:
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
                background_color = self.get_tuple(section.get("BackgroundColor"))
                foreground_color = self.get_tuple(section.get("ForegroundColor"))
                idle_time = section.getint('IdleTime', fallback=self._idle_time)

                if not background_color:
                    background_color = self._background_color
                if not foreground_color:
                    foreground_color = self._foreground_color
                if len(background_color) != 3:
                    raise ExceptionFormat(section.name, "BackgroundColor")
                if len(foreground_color) != 3:
                    raise ExceptionFormat(section.name, "ForegroundColor")

                entry = (start, background_color, foreground_color, idle_time)
                self._time_line.append(entry)
        if not self._time_line:
            entry = (
                datetime.datetime.strptime("00:00:00", "%H:%M:%S"),
                self._background_color,
                self._foreground_color,
                self._idle_time)
            self._time_line.append(entry)
        list.sort(self._time_line, key=lambda entry: entry[0])

    @property
    def FullScreen(self) -> bool:
        return self._config["MAIN"].getboolean("FullScreen", fallback=False)

    def PIR_Pin(self) -> str:
        return self._config["MAIN"].get("PIR")

    def LED_Pin(self) -> str:
        return self._config["MAIN"].get("LED")

    @property
    def configuration(self):
        return self._config

    def get_curret_setting(self):
        value = datetime.datetime.today()
        current = self._time_line[0]
        for line in self._time_line[1:]:
            if value.hour < line[0].hour:
                break
            if value.minute < line[0].minute:
                break
            if value.second < line[0].second:
                break
            current = line
        return current

    def get_tuple(self, value):
        """  Конвертирует строку '0, 0, 0' в кортеж (0, 0, 0) """
        if value is None:
            return None
        return tuple(int(item.strip("([ '])")) for item in value.split(",") if item.strip())
