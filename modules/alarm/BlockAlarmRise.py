import configparser
import datetime

from modules.alarm.AlarmTimeBase import AlarmTimeBase


class BlockAlarmRise(AlarmTimeBase):
    """description of class"""

    def __init__(self, logger, setting):
        """Initializes (declare internal variables)"""
        super(BlockAlarmRise, self).__init__(logger, setting)
        self._startR = None
        self._startG = None
        self._startB = None
        self._stopR = None
        self._stopG = None
        self._stopB = None
        self._stepR = None
        self._stepG = None
        self._stepB = None
        self._currentR = None
        self._currentG = None
        self._currentB = None

    def updateDisplay(self, screen, size, foreColor, backColor, blocks, current_time):
        try:
            if not self._isAlarm:
                return
            backColor = (self._currentR, self._currentG, self._currentB)
            screen.fill(backColor)
            for block in blocks:
                block.updateDisplay(True, screen, size, self._foreColor, backColor, current_time)

            (self._currentR, self._stepR) = self._calculateColorPart(
                self._startR,
                self._stopR,
                self._stepR,
                self._currentR)
            (self._currentG, self._stepG) = self._calculateColorPart(
                self._startG,
                self._stopG,
                self._stepG,
                self._currentG)
            (self._currentB, self._stepB) = self._calculateColorPart(
                self._startB,
                self._stopB,
                self._stepB,
                self._currentB)

        except Exception as ex:
            self._logger.exception(ex)

    def init_draw(self):
        super(BlockAlarmRise, self).init_draw()
        (start, backgroundColor, foregroundColor, idleTime) = self._setting.get_curret_setting()
        self._startR = backgroundColor[0]
        self._startG = backgroundColor[1]
        self._startB = backgroundColor[2]
        self._stopR = self._backColor[0]
        self._stopG = self._backColor[1]
        self._stopB = self._backColor[2]
        self._stepR = (self._stopR - self._startR) / 4
        self._stepG = (self._stopG - self._startG) / 4
        self._stepB = (self._stopB - self._startB) / 4
        self._currentR = self._startR
        self._currentG = self._startG
        self._currentB = self._startB

    def _calculateColorPart(self, start, stop, step, current):
        current += step
        if (current > stop):
            step = -step
            current += step
        if (current < start):
            step = -step
            current += step
        return (current, step)
