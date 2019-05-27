from modules.alarm.alarm_time_file_base import AlarmTimeFileBase


class BlockAlarmSimple(AlarmTimeFileBase):
    """description of class"""

    def update_display(self, screen, size, fore_color, back_color, blocks, current_time):
        try:
            if not self._is_alarm:
                return

            screen.fill(self._back_color)
            for block in blocks:
                block.update_display(True, screen, size, self._fore_color, self._back_color, current_time)

        except Exception as ex:
            self._logger.exception(ex)
