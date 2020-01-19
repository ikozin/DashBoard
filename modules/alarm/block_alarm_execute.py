from exceptions import ExceptionNotFound
from modules.alarm.alarm_time_base import AlarmTimeBase
from logging import Logger


class BlockAlarmExecute(AlarmTimeBase):
    """description of class"""

    def __init__(self, logger: Logger, setting):
        """Initializes (declare internal variables)"""
        super(BlockAlarmExecute, self).__init__(logger, setting)
        self._is_alarm = False
        self._module = None

    def init(self, config_section, mod_list) -> None:
        """Initializes (initialize internal variables)"""
        super(BlockAlarmExecute, self).init(config_section, mod_list)
        module_name = config_section.get("Module")
        if module_name not in mod_list:
            raise ExceptionNotFound(config_section.name, "Module")
        self._module = mod_list[module_name]

    def execute(self) -> None:
        if self._is_alarm:
            return
        self._is_alarm = True
        self._module.execute()
        self._is_alarm = False
