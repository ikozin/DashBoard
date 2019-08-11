import datetime
from exceptions import ExceptionFormat, ExceptionNotFound
from modules.alarm.alarm_base import AlarmBase


class AlarmTimeBase(AlarmBase):
    """description of class"""

    def __init__(self, logger, setting):
        """Initializes (declare internal variables)"""
        super(AlarmTimeBase, self).__init__(logger, setting)
        self._start_time = None
        self._weekday = None
        self._duration = None

    def init(self, config_section, mod_list):
        """Initializes (initialize internal variables)"""
        super(AlarmTimeBase, self).init(config_section, mod_list)

        self._start_time = config_section.get("Time")
        self._weekday = self._get_tuple(config_section.get("WeekDay"))
        self._duration = config_section.getint("Duration")
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

    def update_state(self, current_time):
        # if not isinstance(current_time, datetime.datetime):
        #    raise TypeError("Передаваемый параметр должен быть наследником datetime")
        if any(current_time.weekday() == day for day in self._weekday):
            if (current_time - self._start_time).seconds <= 3:  # 3 секунды на запуск, вдруг задержка какая-нить была
                self.execute()
                return

    def execute(self):
        #  необходима самомтоятельная проверка на повторнй запуск, из-за поправки на задержку в 3 сек.
        pass
