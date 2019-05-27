from abc import ABCMeta, abstractmethod

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

    @abstractmethod
    def init(self, mod_list):
        """Вызывается после создания для начальной инициализации плагина.
           Читаем настройки из конфиг файла.
           Устанавливаем таймер срабатывания для наследников BlockSecondBase и BlockMinuteBase.
           В конце, при необходимости, для обновления информации вызываем update_info(True)"""

    def procced_event(self, event, is_online):
        pass

    def update_info(self, is_online):
        if not is_online:
            return

    def update_display(self, is_online, screen, size, fore_color, back_color, current_time):
        pass

    def add_block(self, block):
        pass

    def execute(self, *args):
        pass

    def get_text(self):
        return self._text

    def done(self):
        """Вызывается перед завершением.
           Освобождаем ресурсы, завершаем потоки и т.п."""

    def _get_tuple(self, value):
        return self._setting.get_tuple(value)
