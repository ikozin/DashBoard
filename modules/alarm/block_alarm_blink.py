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
        self._foreColor = self._getTuple(configSection.get("ForegroudColor"))
        self._backColor = self._getTuple(configSection.get("BackgroudColor"))

        if self._startTime is None: raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(configSection.name, "Time"))
        if self._duration is None:  raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(configSection.name, "Duration"))
        if self._foreColor is None: raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(configSection.name, "ForegroudColor"))
        if self._backColor is None: raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(configSection.name, "BackgroudColor"))

        if len(self._foreColor) != 3: raise Exception(TEXT_EXCEPTION_FORMAT.format(configSection.name, "ForegroudColor"))
        if len(self._backColor) != 3: raise Exception(TEXT_EXCEPTION_FORMAT.format(configSection.name, "BackgroudColor"))

        self._startTime = datetime.datetime.strptime(self._startTime, "%H:%M:%S")
        self._stopTime = self._startTime + datetime.timedelta(seconds = self._duration)


    def updateState(self, currentTime):
        if not isinstance(currentTime, datetime.datetime): raise("Передаваемый параметр должен быть наследником datetime")

        if (currentTime - self._startTime).seconds == 0:
            self._isAlarm = True
        if (currentTime - self._stopTime).seconds == 0:
            self._isAlarm = False


    def updateDisplay(self, screen, size, foreColor, backColor, blocks):
        try:
            if not self._isAlarm: return
            pass
        except Exception as ex:
            self._logger.exception(ex)
