from abc import ABCMeta, abstractclassmethod

from logging import Logger
from setting import Setting


class BlockBase(metaclass=ABCMeta):
    """description of class"""

    def __init__(self, logger, setting):
        """Initializes (declare internal variables)"""
        if not isinstance(logger, Logger):   raise("Передаваемый параметр logger должен быть Logger")
        if not isinstance(setting, Setting): raise("Передаваемый параметр setting должен быть Setting")
        self._logger = logger
        self._setting = setting
        self._text = None


    def __del__(self):
        """Destructor"""
        pass


    @abstractclassmethod
    def init(self, fileName, isOnline, modList):
        """Initializes (initialize internal variables)"""
        pass


    @classmethod
    def proccedEvent(self, event, isOnline):
        """ """
        pass


    @classmethod
    def updateInfo(self, isOnline):
        """ """
        if not isOnline: return
        pass


    @classmethod
    def updateDisplay(self, isOnline, screen, size, foreColor, backColor, current_time):
        """ """
        pass


    @classmethod
    def getText(self):
        """ """
        return self._text


    def _getTuple(self, value):
        return self._setting.getTuple(value, self._logger)
