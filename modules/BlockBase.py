from abc import ABCMeta, abstractclassmethod

from logging import Logger
from setting import Setting


class BlockBase(metaclass=ABCMeta):
    """description of class"""

    def __init__(self, logger, setting):
        """Initializes (declare internal variables)"""
        if not isinstance(logger, Logger):
            raise TypeError("Передаваемый параметр logger должен быть Logger")
        if not isinstance(setting, Setting):
            raise TypeError("Передаваемый параметр setting должен быть Setting")
        self._logger = logger
        self._setting = setting
        self._text = None

    def __del__(self):
        """Destructor"""
        pass

    @abstractclassmethod
    def init(self, modList):
        """Вызывается после создания для начальной инициализации плагина.
           Читаем настройки из конфиг файла.
           Устанавливаем таймер срабатывания для наследников BlockSecondBase и BlockMinuteBase.
           В конце, при необходимости, для обновления информации вызываем updateInfo(True)"""
        pass

    def proccedEvent(self, event, isOnline):
        pass

    def updateInfo(self, isOnline):
        if not isOnline:
            return
        pass

    def updateDisplay(self, isOnline, screen, size, foreColor, backColor, current_time):
        pass

    def addBlock(self, block):
        raise("NotImplemented")

    def execute(self):
        raise("NotImplemented")
    
    def getText(self):
        return self._text

    def done(self):
        """Вызывается перед завершением.
           Освобождаем ресурсы, завершаем потоки и т.п."""
        pass

    def _getTuple(self, value):
        return self._setting.getTuple(value, self._logger)
