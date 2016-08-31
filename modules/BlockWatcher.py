import configparser 
import datetime
import pygame
import pygame.locals
import subprocess
import sys

from exceptions import ExceptionFormat, ExceptionNotFound
from modules.BlockBase import BlockBase
BLOCK_WATCHER_UPDATE_EVENT = (pygame.locals.USEREVENT + 3)


class BlockWatcher(BlockBase):
    """description of class"""

    def __init__(self, logger, setting):
        """Initializes (declare internal variables)"""
        super(BlockWatcher, self).__init__(logger, setting)
        self._startTime = None
        self._stopTime = None
        self._weekDay = None
        self._time = None
        self._path = None


    def init(self, fileName):
        """Initializes (initialize internal variables)"""
        # Загружаем настройки
        config = configparser.ConfigParser()
        config.read(fileName, "utf-8")
        section = config["WatcherBlock"]
        self._weekDay = self._getTuple(section.get("WeekDay"))
        self._startTime = section.get("StartTime")
        self._stopTime = section.get("FinishTime")
        self._time = section.getint("UpdateTime")
        self._path = section.get("Path")

        if self._weekDay is None:   raise ExceptionNotFound(section.name, "WeekDay")
        if self._startTime is None: raise ExceptionNotFound(section.name, "StartTime")
        if self._stopTime is None: raise ExceptionNotFound(section.name, "FinishTime")
        if self._time is None: raise ExceptionNotFound(section.name, "UpdateTime")
        if self._path is None: raise ExceptionNotFound(section.name, "Path")

        if len(self._weekDay) > 7:    raise ExceptionFormat(section.name, "WeekDay")
        if not all(day >= 0 and day < 7 for day in self._weekDay): raise ExceptionFormat(section.name, "WeekDay")
        
        self._startTime = datetime.datetime.strptime(self._startTime, "%H:%M:%S")
        self._stopTime = datetime.datetime.strptime(self._stopTime, "%H:%M:%S")

        ###########################################################################
        if sys.platform == "linux": # Only for Raspberry Pi
            pass
        else:
            self._path = "calc.exe"
        ###########################################################################
        pygame.time.set_timer(BLOCK_WATCHER_UPDATE_EVENT, self._time * 1000)


    def proccedEvent(self, event, isOnline):
        if event.type == BLOCK_WATCHER_UPDATE_EVENT:
            self.updateInfo(isOnline)


    def updateInfo(self, isOnline):
        try:
            if not isOnline: return
            if not self._path: return
            currentTime = datetime.datetime.now()
            if any(currentTime.weekday() == day for day in self._weekDay):
                subprocess.Popen(self._path, shell=True)
        except Exception as ex:
            self._logger.exception(ex)
