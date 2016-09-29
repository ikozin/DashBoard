import os
import configparser
import datetime
import pygame
import pygame.locals

from modules.alarm.AlarmBase import AlarmBase
from exceptions import ExceptionFormat, ExceptionNotFound

ALARM_VOLUME_MIN = 0.1
ALARM_VOLUME_MAX = 1.0
ALARM_VOLUME_STEP = 0.05

class AlarmTimeBase(AlarmBase):
    """description of class"""

    def __init__(self, logger, setting):
        """Initializes (declare internal variables)"""
        super(AlarmTimeBase, self).__init__(logger, setting)
        self._fileName = None
        self._isAlarm = False
        self._startTime = None
        self._stopTime = None
        self._weekDay = None
        self._duration = None
        self._foreColor = None
        self._backColor = None
        self._volume = ALARM_VOLUME_MIN

    def init(self, configSection):
        """Initializes (initialize internal variables)"""
        super(AlarmTimeBase, self).init(configSection)
        
        self._startTime = configSection.get("Time")
        self._weekDay = self._getTuple(configSection.get("WeekDay"))
        self._duration = configSection.getint("Duration")
        self._foreColor = self._getTuple(configSection.get("ForegroundColor"))
        self._backColor = self._getTuple(configSection.get("BackgroundColor"))
        self._fileName = configSection.get("File")
        if self._fileName and not os.path.exists(self._fileName): self._fileName = None

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
                    self._volume = ALARM_VOLUME_MIN
                    self.init_draw()
                    self._isAlarm = True
                    return
        
        if self._isAlarm:
            if (currentTime - self._stopTime).seconds <= 3:
                self.done_draw()
                self._isAlarm = False

        if self._isAlarm:
            if self._volume < ALARM_VOLUME_MAX:
                self._volume += ALARM_VOLUME_STEP
                pygame.mixer.music.set_volume(self._volume)

    def init_draw(self):
        """ """
        if not self._fileName: return
        pygame.mixer.music.set_volume(self._volume)
        pygame.mixer.music.load(self._fileName)
        pygame.mixer.music.play()

        #if not pygame.mixer.get_busy():
        #    soundFile = getvoicetext(self._weather_text)
        #    sound = pygame.mixer.Sound(soundFile)
        #    sound.set_volume(1.0)   # Now plays at 100% of full volume.
        #    sound.play()            # Sound plays at full volume by default


    def done_draw(self):
        """ """
        pass
