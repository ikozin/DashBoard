import configparser

from abc import ABCMeta, abstractmethod
from logging import Logger
from setting import Setting


class AlarmBase(metaclass=ABCMeta):
    """description of class"""

    def __init__(self, logger: Logger, setting: Setting):
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
    def init(self, config_section, mod_list) -> None:
        """Initializes (initialize internal variables)"""
        if not isinstance(config_section, configparser.SectionProxy):
            raise TypeError("Передаваемый параметр должен быть наследником configparser.SectionProxy")

    def update_state(self, current_time) -> None:
        pass

    def update_display(self, screen, size, fore_color, back_color, blocks, current_time) -> None:
        pass

    @abstractmethod
    def execute(self) -> None:
        pass

    def _get_tuple(self, value):
        return self._setting.get_tuple(value)
