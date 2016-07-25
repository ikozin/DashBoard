﻿import configparser 
from logging import Logger
from setting import Setting

class AlarmBase:
    """description of class"""

    def __init__(self, logger, setting):
        """Initializes (declare internal variables)"""
        if not isinstance(logger, Logger):   raise("Передаваемый параметр logger должен быть классом Logger")
        if not isinstance(setting, Setting): raise("Передаваемый параметр setting должен быть классом Setting")
        self._logger = logger
        self._setting = setting


    def __del__(self):
        """Destructor"""
        pass


    def init(self, configSection):
        """Initializes (initialize internal variables)"""
        if not isinstance(configSection, configparser.SectionProxy):
            raise("Передаваемый параметр должен быть наследником configparser.SectionProxy")


    def updateState(self, currentTime):
        pass


    def updateDisplay(self, screen, size, foreColor, backColor, blocks):
        pass


    def _getTuple(self, value):
        return self._setting.getTuple(value, self._logger)