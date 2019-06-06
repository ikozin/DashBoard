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
        self._start_time = None
        self._stop_time = None
        self._weekday = None
        self._path = None
        self._is_watching = False

    def init(self, mod_list):
        """Initializes (initialize internal variables)"""
        # Загружаем настройки
        section = self._setting.configuration["WatcherBlock"]

        self._weekday = self._get_tuple(section.get("WeekDay"))
        self._start_time = section.get("StartTime")
        self._stop_time = section.get("FinishTime")
        self._path = section.get("Path")
        time = section.getint("UpdateTime")

        if self._weekday is None:
            raise ExceptionNotFound(section.name, "WeekDay")
        if self._start_time is None:
            raise ExceptionNotFound(section.name, "StartTime")
        if self._stop_time is None:
            raise ExceptionNotFound(section.name, "FinishTime")
        if self._path is None:
            raise ExceptionNotFound(section.name, "Path")
        if time is None:
            raise ExceptionNotFound(section.name, "UpdateTime")

        if len(self._weekday) > 7:
            raise ExceptionFormat(section.name, "WeekDay")
        if not all(0 <= day < 7 for day in self._weekday):
            raise ExceptionFormat(section.name, "WeekDay")

        self._start_time = datetime.datetime.strptime(self._start_time, "%H:%M:%S")
        self._stop_time = datetime.datetime.strptime(self._stop_time, "%H:%M:%S")

        self.update_info(True)
        self.set_time(time)

    def update_info(self, is_online):
        try:
            if not is_online:
                return
            if not self._path:
                return
            current_time = datetime.datetime.now()
            if not self._is_watching:
                if any(current_time.weekday() == day for day in self._weekday):
                    if current_time.time() >= self._start_time.time():
                        self._is_watching = True
            if self._is_watching:
                self.execute()
                if current_time.time() > self._stop_time.time():
                    self._is_watching = False
        except Exception as ex:
            self._logger.exception(ex)

    def execute(self, *args):
        ###########################################################################
        if sys.platform == "linux":  # Only for Raspberry Pi
            subprocess.Popen(self._path + " > /dev/null 2>&1", shell=True)
            # subprocess.Popen(
            #    self._path,
            #    shell=True,
            #    stdin=subprocess.PIPE,
            #    stdout=subprocess.PIPE,
            #    stderr=subprocess.STDOUT).wait()
        else:
            subprocess.Popen("calc.exe", shell=True)
        ###########################################################################
