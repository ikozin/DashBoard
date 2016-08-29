import configparser 
import datetime
import pygame
import pygame.locals

from exceptions import ExceptionFormat, ExceptionNotFound
from modules.BlockBase import BlockBase

class BlockWatcher(BlockBase):
    """description of class"""

    def __init__(self, logger, setting):
        """Initializes (declare internal variables)"""
        super(BlockWatcher, self).__init__(logger, setting)
        self._path = None
        self._lastUpdate = datetime.datetime.now()


    def init(self, fileName):
        """Initializes (initialize internal variables)"""
        # Загружаем настройки
        #config = configparser.ConfigParser()
        #config.read(fileName, "utf-8")
        #section = config["WatcherBlock"]
        self._path = "~/webcam.sh"
        #self._path = section.get("Path")
        #if self._path is None:     raise ExceptionNotFound(section.name, "Path")


    def updateInfo(self, isOnline):
        try:
            if not isOnline: return
            if not self._path: return
            if (datetime.datetime.now() - self._lastUpdate).seconds <= 5: return
            self._lastUpdate = datetime.datetime.now()
            subprocess.Popen(self._path, shell=True)
            pass
        except Exception as ex:
            self._logger.exception(ex)
