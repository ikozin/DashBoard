from exceptions import ExceptionNotFound
from modules.alarm.AlarmTimeBase import AlarmTimeBase


class BlockAlarmExecute(AlarmTimeBase):
    """description of class"""

    def __init__(self, logger, setting):
        """Initializes (declare internal variables)"""
        super(BlockAlarmExecute, self).__init__(logger, setting)
        self._isAlarm = False
        self._modList = None
        self._module = None

    def init(self, configSection, modList):
        """Initializes (initialize internal variables)"""
        super(BlockAlarmExecute, self).init(configSection, modList)
        self._modList = modList
        self._module = configSection.get("Module")
        if self._module not in self._modList:
            raise ExceptionNotFound(configSection.name, "Module")

    def execute(self):
        if self._isAlarm:
            return
        self._isAlarm = True
        self._modList[self._module].execute()
        self._isAlarm = False
