from logging import Logger
from setting import Setting


class BlockBase:
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


    def init(self, fileName, isOnline, modList):
        """Initializes (initialize internal variables)"""
        pass


    def proccedEvent(self, event, isOnline):
        """ """
        pass


    def updateInfo(self, isOnline):
        """ """
        if not isOnline: return
        pass


    def updateDisplay(self, isOnline, screen, size, foreColor, backColor, current_time):
        """ """
        pass


    def getText(self):
        """ """
        return self._text


    def _getTuple(self, value):
        return self._setting.getTuple(value, self._logger)
