from setting import BLOCK_SECOND_UPDATE_EVENT
from modules.BlockBase import BlockBase
from logging import Logger


class BlockSecondBase(BlockBase):
    """description of class"""

    def __init__(self, logger: Logger, setting):
        """Initializes (declare internal variables)"""
        super(BlockSecondBase, self).__init__(logger, setting)
        self._time = None
        self._time_value = None

    def set_time(self, value):
        self._time = value
        self._time_value = value

    def procced_event(self, event, is_online):
        if event.type == BLOCK_SECOND_UPDATE_EVENT:
            self._time_value -= 1
            if not self._time_value:
                self._time_value = self._time
                self.update_info(is_online)
