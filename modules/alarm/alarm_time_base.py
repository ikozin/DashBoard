import configparser
import datetime

from modules.alarm.alarm_base import AlarmBase
from exceptions import ExceptionFormat, ExceptionNotFound

class AlarmTimeBase(AlarmBase):
    """description of class"""

    def __init__(self, logger):
        """Initializes (declare internal variables)"""
        super(AlarmTimeBase, self).__init__(logger)
        self._isAlarm = False
        self._startTime = None
        self._stopTime = None
        self._duration = None
        self._foreColor = None
        self._backColor = None


    def init(self, configSection):
        """Initializes (initialize internal variables)"""
        super(AlarmTimeBase, self).init(configSection)
        
        self._startTime = configSection.get("Time")
        self._duration = configSection.getint("Duration")
        self._foreColor = self._getTuple(configSection.get("ForegroundColor"))
        self._backColor = self._getTuple(configSection.get("BackgroundColor"))

        if self._startTime is None: raise ExceptionNotFound(configSection.name, "Time")
        if self._duration is None:  raise ExceptionNotFound(configSection.name, "Duration")
        if self._foreColor is None: raise ExceptionNotFound(configSection.name, "ForegroundColor")
        if self._backColor is None: raise ExceptionNotFound(configSection.name, "BackgroundColor")

        if len(self._foreColor) != 3: raise ExceptionFormat(configSection.name, "ForegroundColor")
        if len(self._backColor) != 3: raise ExceptionFormat(configSection.name, "BackgroundColor")

        self._startTime = datetime.datetime.strptime(self._startTime, "%H:%M:%S")
        self._stopTime = self._startTime + datetime.timedelta(seconds = self._duration)
        print(self._startTime, self._stopTime)


    def updateState(self, currentTime):
        #if not isinstance(currentTime, datetime.datetime): raise("Передаваемый параметр должен быть наследником datetime")

        if not self._isAlarm:
            if (currentTime - self._startTime).seconds <= 3: #3 секунды на запуск, вдруг задержка какая-нить была
                self._isAlarm = True
                print(self._startTime, currentTime, self._isAlarm)
                return
        
        if self._isAlarm:
            if (currentTime - self._stopTime).seconds <= 3:
                self._isAlarm = False
                print(self._startTime, currentTime, self._isAlarm)
                return
