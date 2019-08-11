import datetime
from exceptions import ExceptionNotFound
from modules.alarm.alarm_time_base import AlarmTimeBase


class BlockAlarmText(AlarmTimeBase):
    """description of class"""

    def __init__(self, logger, setting):
        """Initializes (declare internal variables)"""
        super(BlockAlarmText, self).__init__(logger, setting)
        self._is_alarm = False
        self._fore_color = None
        self._back_color = None
        self._module = None
        self._text = None

    def init(self, config_section, mod_list):
        """Initializes (initialize internal variables)"""
        super(BlockAlarmText, self).init(config_section, mod_list)
        if "Voice" not in mod_list:
            raise ExceptionNotFound(config_section.name, "Voice")
        self._module = mod_list["Voice"]
        self._fore_color = self._get_tuple(config_section.get("ForegroundColor"))
        self._back_color = self._get_tuple(config_section.get("BackgroundColor"))
        self._text = config_section.get("Text")
        if self._fore_color is None:
            raise ExceptionNotFound(config_section.name, "ForegroundColor")
        if self._back_color is None:
            raise ExceptionNotFound(config_section.name, "BackgroundColor")
        if len(self._fore_color) != 3:
            raise ExceptionFormat(config_section.name, "ForegroundColor")
        if len(self._back_color) != 3:
            raise ExceptionFormat(config_section.name, "BackgroundColor")
        if self._text is None:
            raise ExceptionNotFound(config_section.name, "Text")

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
        self._module.execute(self._text)
        self._is_alarm = False
