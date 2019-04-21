import configparser
import datetime

from modules.alarm.AlarmTimeBase import AlarmTimeBase


class BlockAlarmExecute(AlarmTimeBase):
    """description of class"""

    def updateDisplay(self, screen, size, foreColor, backColor, blocks, current_time):
        try:
            if not self._isAlarm:
                return

            screen.fill(self._backColor)
            for block in blocks:
                block.updateDisplay(True, screen, size, self._foreColor, self._backColor, current_time)

        except Exception as ex:
            self._logger.exception(ex)
