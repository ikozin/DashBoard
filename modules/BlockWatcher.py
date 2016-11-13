import configparser
import datetime
import subprocess
import sys

from exceptions import ExceptionFormat, ExceptionNotFound
from modules.BlockSecondBase import BlockSecondBase


class BlockWatcher(BlockSecondBase):
    """description of class"""

    def __init__(self, logger, setting):
        """Initializes (declare internal variables)"""
        super(BlockWatcher, self).__init__(logger, setting)
        self._startTime = None
        self._stopTime = None
        self._weekDay = None
        self._path = None
        self._isWatching = False


    def init(self, fileName, isOnline, modList):
        """Initializes (initialize internal variables)"""
        # Загружаем настройки
        config = configparser.ConfigParser()
        config.read(fileName, "utf-8")
        section = config["WatcherBlock"]
        self._weekDay = self._getTuple(section.get("WeekDay"))
        self._startTime = section.get("StartTime")
        self._stopTime = section.get("FinishTime")
        self._path = section.get("Path")
        time = section.getint("UpdateTime")

        if self._weekDay is None:   raise ExceptionNotFound(section.name, "WeekDay")
        if self._startTime is None: raise ExceptionNotFound(section.name, "StartTime")
        if self._stopTime is None:  raise ExceptionNotFound(section.name, "FinishTime")
        if self._path is None:      raise ExceptionNotFound(section.name, "Path")
        if time is None:            raise ExceptionNotFound(section.name, "UpdateTime")

        if len(self._weekDay) > 7:  raise ExceptionFormat(section.name, "WeekDay")
        if not all(day >= 0 and day < 7 for day in self._weekDay): raise ExceptionFormat(section.name, "WeekDay")

        self._startTime = datetime.datetime.strptime(self._startTime, "%H:%M:%S")
        self._stopTime = datetime.datetime.strptime(self._stopTime, "%H:%M:%S")

        self.updateInfo(isOnline)
        self.setTime(time)


    def updateInfo(self, isOnline):
        try:
            if not isOnline: return
            if not self._path: return
            currentTime = datetime.datetime.now()
            if not self._isWatching:
                if any(currentTime.weekday() == day for day in self._weekDay):
                    if currentTime.time() >= self._startTime.time():
                        self._isWatching = True
            if self._isWatching:
                if currentTime.time() > self._stopTime.time():
                    self._isWatching = False
            if self._isWatching:
                ###########################################################################
                if sys.platform == "linux": # Only for Raspberry Pi
                    subprocess.Popen(self._path + " > /dev/null 2>&1", shell=True)
                    #subprocess.Popen(self._path, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).wait()
                else:
                    subprocess.Popen("calc.exe", shell=True)
                ###########################################################################
        except Exception as ex:
            self._logger.exception(ex)
