import os

from exceptions import ExceptionFormat, ExceptionNotFound
from modules.alarm.alarm_time_base import AlarmTimeBase
from logging import Logger
from setting import Setting


class AlarmTimeFileBase(AlarmTimeBase):
    """description of class"""

    def __init__(self, logger: Logger, setting: Setting):
        """Initializes (declare internal variables)"""
        super(AlarmTimeFileBase, self).__init__(logger, setting)
        self._file_name = None
        self._fore_color = None
        self._back_color = None
        self._is_alarm = False
        self._volume_max = 0
        self._volume_cur = 0
        self._volume = None
        self._player = None

    def init(self, config_section, mod_list) -> None:
        """Initializes (initialize internal variables)"""
        super(AlarmTimeFileBase, self).init(config_section, mod_list)

        self._fore_color = self._get_tuple(config_section.get("ForegroundColor"))
        self._back_color = self._get_tuple(config_section.get("BackgroundColor"))
        self._file_name = config_section.get("File")
        if self._file_name and not os.path.exists(self._file_name):
            self._file_name = None

        if self._fore_color is None:
            raise ExceptionNotFound(config_section.name, "ForegroundColor")
        if self._back_color is None:
            raise ExceptionNotFound(config_section.name, "BackgroundColor")
        if len(self._fore_color) != 3:
            raise ExceptionFormat(config_section.name, "ForegroundColor")
        if len(self._back_color) != 3:
            raise ExceptionFormat(config_section.name, "BackgroundColor")

        self._volume = mod_list["Volume"]
        self._player = mod_list["Player"]
        if self._volume is None:
            raise ExceptionFormat(config_section.name, "Volume")
        if self._player is None:
            raise ExceptionFormat(config_section.name, "Player")

    def update_state(self, current_time) -> None:
        super(AlarmTimeFileBase, self).update_state(current_time)
        if self._is_alarm:
            if (current_time - self._stop_time).seconds <= 3:
                self._volume_max = self._volume.execute(self._volume_max)
                self._is_alarm = False
        if self._is_alarm:
            if self._volume_cur < self._volume_max:
                self._volume_cur = self._volume.execute("+")

    def execute(self) -> None:
        if self._is_alarm:
            return
        self.init_draw()
        self._volume_max = self._volume.execute()
        self._volume_cur = self._volume.execute(0)
        if self._file_name:
            self._player.execute(self._file_name)
        self._is_alarm = True

    def init_draw(self):
        pass

    def done_draw(self):
        pass
