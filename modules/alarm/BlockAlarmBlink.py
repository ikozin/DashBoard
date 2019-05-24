import datetime

from modules.alarm.AlarmTimeFileBase import AlarmTimeFileBase


class BlockAlarmBlink(AlarmTimeFileBase):
    """description of class"""

    def updateDisplay(self, screen, size, foreColor, backColor, blocks, current_time):
        try:
            if not self._isAlarm:
                return

            value = datetime.datetime.today()
            if (value - self._startTime).seconds % 2 == 0:
                backColor = self._backColor

            screen.fill(backColor)
            for block in blocks:
                block.updateDisplay(True, screen, size, self._foreColor, backColor, current_time)

        except Exception as ex:
            self._logger.exception(ex)
