from setting import BLOCK_SECOND_UPDATE_EVENT
from modules.BlockBase import BlockBase
from logging import Logger
from setting import Setting


class BlockSecondBase(BlockBase):
    """description of class"""

    def __init__(self, logger: Logger, setting: Setting):
        """Initializes (declare internal variables)"""
        super(BlockSecondBase, self).__init__(logger, setting)
        self._timer: int = 0
        self._timer_value: int = 0

    def set_time(self, value: int) -> None:
        self._timer = value
        self._timer_value = value

    def procced_event(self, event, is_online: bool) -> None:
        if event.type == BLOCK_SECOND_UPDATE_EVENT:
            self._timer_value -= 1
            if not self._timer_value:
                self._timer_value = self._timer
                self.update_info(is_online)
