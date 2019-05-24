﻿import configparser
from abc import ABCMeta, abstractmethod
from logging import Logger
from setting import Setting


class AlarmBase(metaclass=ABCMeta):
    """description of class"""

    def __init__(self, logger, setting):
        """Initializes (declare internal variables)"""
        if not isinstance(logger, Logger):
            raise TypeError("Передаваемый параметр logger должен быть классом Logger")
        if not isinstance(setting, Setting):
            raise TypeError("Передаваемый параметр setting должен быть классом Setting")
        self._logger = logger
        self._setting = setting

    def __del__(self):
        """Destructor"""

    @abstractmethod
    def init(self, configSection, modList):
        """Initializes (initialize internal variables)"""
        if not isinstance(configSection, configparser.SectionProxy):
            raise TypeError("Передаваемый параметр должен быть наследником configparser.SectionProxy")

    def updateState(self, currentTime):
        pass

    def updateDisplay(self, screen, size, foreColor, backColor, blocks, current_time):
        pass

    @abstractmethod
    def execute(self):
        pass

    def _getTuple(self, value):
        return self._setting.getTuple(value)
