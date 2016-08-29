import configparser 
import pygame
import pygame.locals

from exceptions import ExceptionFormat, ExceptionNotFound
from modules.BlockBase import BlockBase

class BlockWatcher(BlockBase):
    """description of class"""

    def __init__(self, logger, setting):
        """Initializes (declare internal variables)"""
        super(BlockWatcher, self).__init__(logger, setting)


    def init(self, fileName):
        """Initializes (initialize internal variables)"""
        # Загружаем настройки
        config = configparser.ConfigParser()
        config.read(fileName, "utf-8")
        section = config["WatcherBlock"]


    def updateInfo(self, isOnline):
        try:
            if not isOnline: return
            pass
        except Exception as ex:
            self._logger.exception(ex)
