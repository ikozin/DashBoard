from setting import BLOCK_MINUTE_UPDATE_EVENT
from modules.BlockBase import BlockBase
from logging import Logger
from setting import Setting


class BlockMinuteBase(BlockBase):
    """description of class"""

    def __init__(self, logger: Logger, setting: Setting):
        """Initializes (declare internal variables)"""
        super(BlockMinuteBase, self).__init__(logger, setting)
        self._time: int = 1
        self._time_value: int = 1

    def set_time(self, value: int) -> None:
        self._time = value
        self._time_value = value

    def procced_event(self, event, is_online: bool) -> None:
        if event.type == BLOCK_MINUTE_UPDATE_EVENT:
            self._time_value -= 1
            if not self._time_value:
                self._time_value = self._time
                self.update_info(is_online)
