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
        self._time = None
        self._path = None


    def init(self, fileName):
        """Initializes (initialize internal variables)"""
        # Загружаем настройки
        config = configparser.ConfigParser()
        config.read(fileName, "utf-8")
        section = config["WatcherBlock"]
        self._time = section.getint("UpdateTime")
        self._path = section.get("Path")

        if self._time is None: raise ExceptionNotFound(section.name, "UpdateTime")
        if self._path is None: raise ExceptionNotFound(section.name, "Path")
        ###########################################################################
        if sys.platform == "linux": # Only for Raspberry Pi
            self._path = "~/webcam.sh"
        else:
            self._path = "calc.exe"
        ###########################################################################
        pygame.time.set_timer(BLOCK_WATCHER_UPDATE_EVENT, self._time * 60000)


    def proccedEvent(self, event, isOnline):
        if event.type == BLOCK_WATCHER_UPDATE_EVENT:
            self.updateInfo(isOnline)


    def updateInfo(self, isOnline):
        try:
            if not isOnline: return
            if not self._path: return
            subprocess.Popen(self._path, shell=True)
        except Exception as ex:
            self._logger.exception(ex)
