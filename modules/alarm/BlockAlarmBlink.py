import configparser
import datetime

from modules.alarm.AlarmTimeBase import AlarmTimeBase

class BlockAlarmBlink(AlarmTimeBase):
    """description of class"""

    def updateDisplay(self, screen, size, foreColor, backColor, blocks):
        try:
            if not self._isAlarm: return

            value = datetime.datetime.today()
            if (value - self._startTime).seconds % 2 == 0:
                backColor = self._backColor

            screen.fill(backColor)
            for block in blocks:
                block.updateDisplay(True, screen, size, self._foreColor, backColor)

        except Exception as ex:
            self._logger.exception(ex)
