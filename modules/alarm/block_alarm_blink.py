import datetime
from modules.alarm.alarm_time_file_base import AlarmTimeFileBase


class BlockAlarmBlink(AlarmTimeFileBase):
    """description of class"""

    def update_display(self, screen, size, fore_color, back_color, blocks, current_time) -> None:
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
