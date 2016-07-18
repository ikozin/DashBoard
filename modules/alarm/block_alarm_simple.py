import configparser
import datetime

from modules.alarm.alarm_time_base import AlarmTimeBase
from setting import TEXT_EXCEPTION_NOT_FOUND
from setting import TEXT_EXCEPTION_FORMAT

class BlockAlarmSimple(AlarmTimeBase):
    """description of class"""

    def updateDisplay(self, screen, size, foreColor, backColor, blocks):
        try:
            if not self._isAlarm: return

            screen.fill(self._backColor)
            for block in blocks:
                block.updateDisplay(True, screen, size, self._foreColor, self._backColor)

        except Exception as ex:
            self._logger.exception(ex)
