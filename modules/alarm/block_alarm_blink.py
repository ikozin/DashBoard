import configparser
import datetime

from modules.alarm.alarm_base import AlarmBase
from setting import TEXT_EXCEPTION_NOT_FOUND
from setting import TEXT_EXCEPTION_FORMAT

class BlockAlarmBlink(AlarmBase):
    """description of class"""

    def __init__(self, logger):
        """Initializes (declare internal variables)"""
        super(BlockAlarmBlink, self).__init__(logger)
        self._isAlarm = False
        self._startTime = None
        self._stopTime = None
        self._duration = None
        self._foreColor = None
        self._backColor = None


    def init(self, configSection):
        """Initializes (initialize internal variables)"""
        super(BlockAlarmBlink, self).init(configSection)
        
        self._startTime = configSection.get("Time")
        self._duration = configSection.getint("Duration")
        self._foreColor = self._getTuple(configSection.get("ForegroundColor"))
        self._backColor = self._getTuple(configSection.get("BackgroundColor"))

        if self._startTime is None: raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(configSection.name, "Time"))
        if self._duration is None:  raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(configSection.name, "Duration"))
        if self._foreColor is None: raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(configSection.name, "ForegroundColor"))
        if self._backColor is None: raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(configSection.name, "BackgroundColor"))

        if len(self._foreColor) != 3: raise Exception(TEXT_EXCEPTION_FORMAT.format(configSection.name, "ForegroundColor"))
        if len(self._backColor) != 3: raise Exception(TEXT_EXCEPTION_FORMAT.format(configSection.name, "BackgroundColor"))

        self._startTime = datetime.datetime.strptime(self._startTime, "%H:%M:%S")
        self._stopTime = self._startTime + datetime.timedelta(seconds = self._duration)


    def updateState(self, currentTime):
        #if not isinstance(currentTime, datetime.datetime): raise("Передаваемый параметр должен быть наследником datetime")

        if not self._isAlarm:
            if (currentTime - self._startTime).seconds < 3: #3 секунды на запуск, вдруг задержка какая-нить была
                self._isAlarm = True
                return
        
        if self._isAlarm:
            if (currentTime - self._stopTime).seconds >= 0:
                self._isAlarm = False


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
