from exceptions import ExceptionNotFound
from modules.alarm.alarm_time_base import AlarmTimeBase


class BlockAlarmExecute(AlarmTimeBase):
    """description of class"""

    def __init__(self, logger, setting):
        """Initializes (declare internal variables)"""
        super(BlockAlarmExecute, self).__init__(logger, setting)
        self._is_alarm = False
        self._mod_list = None
        self._module = None

    def init(self, config_section, mod_list):
        """Initializes (initialize internal variables)"""
        super(BlockAlarmExecute, self).init(config_section, mod_list)
        self._mod_list = mod_list
        self._module = config_section.get("Module")
        if self._module not in self._mod_list:
            raise ExceptionNotFound(config_section.name, "Module")

    def execute(self):
        if self._is_alarm:
            return
        self._is_alarm = True
        self._mod_list[self._module].execute()
        self._is_alarm = False
