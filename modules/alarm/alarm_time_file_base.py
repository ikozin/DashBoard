import os
import datetime
from exceptions import ExceptionFormat, ExceptionNotFound
import pygame
import pygame.locals
from modules.alarm.alarm_time_base import AlarmTimeBase

ALARM_VOLUME_MIN = 0.2
ALARM_VOLUME_MAX = 1.0
ALARM_VOLUME_STEP = 0.1


class AlarmTimeFileBase(AlarmTimeBase):
    """description of class"""

    def __init__(self, logger, setting):
        """Initializes (declare internal variables)"""
        super(AlarmTimeFileBase, self).__init__(logger, setting)
        self._file_name = None
        self._stop_time = None
        self._duration = None
        self._fore_color = None
        self._back_color = None
        self._volume = ALARM_VOLUME_MIN
        self._is_alarm = False

    def init(self, config_section, mod_list):
        """Initializes (initialize internal variables)"""
        super(AlarmTimeFileBase, self).init(config_section, mod_list)

        self._duration = config_section.getint("Duration")
        self._fore_color = self._get_tuple(config_section.get("ForegroundColor"))
        self._back_color = self._get_tuple(config_section.get("BackgroundColor"))
        self._file_name = config_section.get("File")
        if self._file_name and not os.path.exists(self._file_name):
            self._file_name = None

        if self._duration is None:
            raise ExceptionNotFound(config_section.name, "Duration")
        if self._fore_color is None:
            raise ExceptionNotFound(config_section.name, "ForegroundColor")
        if self._back_color is None:
            raise ExceptionNotFound(config_section.name, "BackgroundColor")
        if len(self._fore_color) != 3:
            raise ExceptionFormat(config_section.name, "ForegroundColor")
        if len(self._back_color) != 3:
            raise ExceptionFormat(config_section.name, "BackgroundColor")
        if len(self._weekday) > 7:
            raise ExceptionFormat(config_section.name, "WeekDay")
        if not all(day >= 0 and day < 7 for day in self._weekday):
            raise ExceptionFormat(config_section.name, "WeekDay")

        self._stop_time = self._start_time + datetime.timedelta(seconds=self._duration)

    def update_state(self, current_time):
        super(AlarmTimeFileBase, self).update_state(current_time)
        if self._is_alarm:
            if (current_time - self._stop_time).seconds <= 3:
                self.done_draw()
                self._is_alarm = False
        if self._is_alarm:
            if self._volume < ALARM_VOLUME_MAX:
                self._volume += ALARM_VOLUME_STEP
                pygame.mixer.music.set_volume(self._volume)

    def execute(self):
        if self._is_alarm:
            return
        self._volume = ALARM_VOLUME_MIN
        self.init_draw()
        self._is_alarm = True

    def init_draw(self):
        if not self._file_name:
            return
        pygame.mixer.music.set_volume(self._volume)
        pygame.mixer.music.load(self._file_name)
        pygame.mixer.music.play()
        # if not pygame.mixer.get_busy():
        #    soundFile = getvoicetext(self._weather_text)
        #    sound = pygame.mixer.Sound(soundFile)
        #    sound.set_volume(1.0)   # Now plays at 100% of full volume.
        #    sound.play()            # Sound plays at full volume by default

    def done_draw(self):
        pass
