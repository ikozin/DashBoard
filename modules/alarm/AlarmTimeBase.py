import datetime

from modules.alarm.AlarmBase import AlarmBase
from exceptions import ExceptionFormat, ExceptionNotFound


class AlarmTimeBase(AlarmBase):
    """description of class"""

    def __init__(self, logger, setting):
        """Initializes (declare internal variables)"""
        super(AlarmTimeBase, self).__init__(logger, setting)
        self._startTime = None
        self._weekDay = None

    def init(self, configSection, modList):
        """Initializes (initialize internal variables)"""
        super(AlarmTimeBase, self).init(configSection, modList)
        self._startTime = configSection.get("Time")
        self._weekDay = self._getTuple(configSection.get("WeekDay"))
        if self._startTime is None:
            raise ExceptionNotFound(configSection.name, "Time")
        if self._weekDay is None:
            raise ExceptionNotFound(configSection.name, "WeekDay")
        if len(self._weekDay) > 7:
            raise ExceptionFormat(configSection.name, "WeekDay")
        if not all(day >= 0 and day < 7 for day in self._weekDay):
            raise ExceptionFormat(configSection.name, "WeekDay")
        self._startTime = datetime.datetime.strptime(self._startTime, "%H:%M:%S")

    def updateState(self, currentTime):
        # if not isinstance(currentTime, datetime.datetime):
        #    raise TypeError("Передаваемый параметр должен быть наследником datetime")
        if any(currentTime.weekday() == day for day in self._weekDay):
            if (currentTime - self._startTime).seconds <= 3:  # 3 секунды на запуск, вдруг задержка какая-нить была
                self.execute()
                return

    def execute(self):
        #  необходима самомтоятельная проверка на повторнй запуск, из-за поправки на задержку в 3 сек.
        pass
