import datetime

from exceptions import ExceptionFormat, ExceptionNotFound
from modules.alarm.alarm_base import AlarmBase
from logging import Logger
from setting import Setting


class AlarmTimeBase(AlarmBase):
    """description of class"""

    def __init__(self, logger: Logger, setting: Setting):
        """Initializes (declare internal variables)"""
        super(AlarmTimeBase, self).__init__(logger, setting)
        self._start_time = None
        self._stop_time = None
        self._weekday = None
        self._duration = 0.0

    def init(self, config_section, mod_list) -> None:
        """Initializes (initialize internal variables)"""
        super(AlarmTimeBase, self).init(config_section, mod_list)

        self._start_time = config_section.get("Time")
        self._weekday = self._get_tuple(config_section.get("WeekDay"))
        self._duration = config_section.getfloat("Duration")
        if self._start_time is None:
            raise ExceptionNotFound(config_section.name, "Time")
        if self._weekday is None:
            raise ExceptionNotFound(config_section.name, "WeekDay")
        if len(self._weekday) > 7:
            raise ExceptionFormat(config_section.name, "WeekDay")
        if not all(0 <= day < 7 for day in self._weekday):
            raise ExceptionFormat(config_section.name, "WeekDay")
        if self._duration is None:
            raise ExceptionNotFound(config_section.name, "Duration")
        self._start_time = datetime.datetime.strptime(self._start_time, "%H:%M:%S")
        self._stop_time = self._start_time + datetime.timedelta(seconds=self._duration)

    def update_state(self, current_time) -> None:
        # if not isinstance(current_time, datetime.datetime):
        #    raise TypeError("Передаваемый параметр должен быть наследником datetime")
        if any(current_time.weekday() == day for day in self._weekday):
            if (current_time - self._start_time).seconds <= 3:  # 3 секунды на запуск, вдруг задержка какая-нить была
                self.execute()
                return

    def execute(self) -> None:
        #  необходима самомтоятельная проверка на повторнй запуск, из-за поправки на задержку в 3 сек.
        pass
