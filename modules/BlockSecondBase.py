from setting import BLOCK_SECOND_UPDATE_EVENT
from modules.BlockBase import BlockBase


class BlockSecondBase(BlockBase):
    """description of class"""

    def __init__(self, logger, setting):
        """Initializes (declare internal variables)"""
        super(BlockSecondBase, self).__init__(logger, setting)
        self._time = None
        self._timeValue = None

    def setTime(self, value):
        self._time = value
        self._timeValue = value

    def proccedEvent(self, event, isOnline):
        if event.type == BLOCK_SECOND_UPDATE_EVENT:
            self._timeValue -= 1
            if (not self._timeValue):
                self._timeValue = self._time
                self.updateInfo(isOnline)
