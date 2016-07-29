import configparser
import datetime
import pygame
import pygame.locals

from modules.alarm.AlarmBase import AlarmBase
from exceptions import ExceptionFormat, ExceptionNotFound

class AlarmTimeBase(AlarmBase):
    """description of class"""

    def __init__(self, logger, setting):
        """Initializes (declare internal variables)"""
        super(AlarmTimeBase, self).__init__(logger, setting)
        self._isAlarm = False
        self._startTime = None
        self._stopTime = None
        self._weekDay = None
        self._duration = None
        self._foreColor = None
        self._backColor = None


    def init(self, configSection):
        """Initializes (initialize internal variables)"""
        super(AlarmTimeBase, self).init(configSection)
        
        self._startTime = configSection.get("Time")
        self._weekDay = self._getTuple(configSection.get("WeekDay"))
        self._duration = configSection.getint("Duration")
        self._foreColor = self._getTuple(configSection.get("ForegroundColor"))
        self._backColor = self._getTuple(configSection.get("BackgroundColor"))

        if self._startTime is None: raise ExceptionNotFound(configSection.name, "Time")
        if self._weekDay is None:   raise ExceptionNotFound(configSection.name, "WeekDay")
        if self._duration is None:  raise ExceptionNotFound(configSection.name, "Duration")
        if self._foreColor is None: raise ExceptionNotFound(configSection.name, "ForegroundColor")
        if self._backColor is None: raise ExceptionNotFound(configSection.name, "BackgroundColor")

        if len(self._foreColor) != 3: raise ExceptionFormat(configSection.name, "ForegroundColor")
        if len(self._backColor) != 3: raise ExceptionFormat(configSection.name, "BackgroundColor")
        
        if len(self._weekDay) > 7:    raise ExceptionFormat(configSection.name, "WeekDay")
        if not all(day >= 0 and day < 7 for day in self._weekDay): raise ExceptionFormat(configSection.name, "WeekDay")

        self._startTime = datetime.datetime.strptime(self._startTime, "%H:%M:%S")
        self._stopTime = self._startTime + datetime.timedelta(seconds = self._duration)


    def updateState(self, currentTime):
        #if not isinstance(currentTime, datetime.datetime): raise("Передаваемый параметр должен быть наследником datetime")

        if not self._isAlarm:
            if any(currentTime.weekday() == day for day in self._weekDay):
                if (currentTime - self._startTime).seconds <= 3: # 3 секунды на запуск, вдруг задержка какая-нить была
                    self.init_draw()
                    self._isAlarm = True
                    return
        
        if self._isAlarm:
            if (currentTime - self._stopTime).seconds <= 3:
                self.done_draw()
                self._isAlarm = False


    def init_draw(self):
        """ """
        pygame.mixer.music.load("music/happy three frend.mp3")
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play()


    def done_draw(self):
        """ """
        pass
