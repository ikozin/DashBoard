from exceptions import ExceptionNotFound
from modules.alarm.alarm_time_base import AlarmTimeBase


class BlockAlarmText(AlarmTimeBase):
    """description of class"""

    def __init__(self, logger, setting):
        """Initializes (declare internal variables)"""
        super(BlockAlarmText, self).__init__(logger, setting)
        self._is_alarm = False

    def init(self, config_section, mod_list):
        """Initializes (initialize internal variables)"""
        super(BlockAlarmExecute, self).init(config_section, mod_list)
        #self._mod_list = mod_list
        #self._module = config_section.get("Module")
        #if self._module not in self._mod_list:
        #    raise ExceptionNotFound(config_section.name, "Module")

    def update_display(self, screen, size, fore_color, back_color, blocks, current_time):
        try:
            if not self._is_alarm:
                return

            value = datetime.datetime.today()
            if (value - self._start_time).seconds % 2 == 0:
                back_color = self._back_color

            screen.fill(back_color)
            for block in blocks:
                block.update_display(True, screen, size, self._fore_color, back_color, current_time)

        except Exception as ex:
            self._logger.exception(ex)

    def execute(self):
        if self._is_alarm:
            return
        self._is_alarm = True
        #self._mod_list[self._module].execute()
        self._is_alarm = False
