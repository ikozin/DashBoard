from typing import Dict, Any
from abc import ABCMeta, abstractmethod
from logging import Logger
from setting import Setting


class BlockBase(metaclass=ABCMeta):
    """description of class"""

    def __init__(self, logger: Logger, setting: Setting):
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
    def init(self, mod_list: Dict[str, 'BlockBase']) -> None:
        """Вызывается после создания для начальной инициализации плагина.
           Читаем настройки из конфиг файла.
           Устанавливаем таймер срабатывания для наследников BlockSecondBase и BlockMinuteBase.
           В конце, при необходимости, для обновления информации вызываем update_info(True)"""

    def procced_event(self, event, is_online: bool) -> None:
        pass

    def update_info(self, is_online: bool) -> None:
        if not is_online:
            return

    def update_display(self, is_online: bool, screen, size, fore_color, back_color, current_time) -> None:
        pass

    def add_block(self, block: 'BlockBase') -> None:
        pass

    def execute(self, *args) -> Any:
        pass

    def get_text(self) -> str:
        return self._text

    def done(self) -> None:
        """Вызывается перед завершением.
           Освобождаем ресурсы, завершаем потоки и т.п."""

    def calc_position(self, text_size, position, align_x, align_y):
        text_x = position[0]  # Left
        if align_x == "Center":
            text_x = position[0] - (text_size[0] >> 1)
        if align_x == "Right":
            text_x = position[0] - text_size[0]

        text_y = position[1]  # Top
        if align_y == "Center":
            text_y = position[1] - (text_size[1] >> 1)
        if align_y == "Bottom":
            text_y = position[1] - text_size[1]

        return (text_x, text_y)

    def _get_tuple(self, value: str):
        return self._setting.get_tuple(value)
