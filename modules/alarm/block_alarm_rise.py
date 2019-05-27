from modules.alarm.alarm_time_file_base import AlarmTimeFileBase


class BlockAlarmRise(AlarmTimeFileBase):
    """description of class"""

    def __init__(self, logger, setting):
        """Initializes (declare internal variables)"""
        super(BlockAlarmRise, self).__init__(logger, setting)
        self._start_r = None
        self._start_g = None
        self._start_b = None
        self._stop_r = None
        self._stop_g = None
        self._stop_b = None
        self._step_r = None
        self._step_g = None
        self._step_b = None
        self._current_r = None
        self._current_g = None
        self._current_b = None

    def update_display(self, screen, size, fore_color, back_color, blocks, current_time):
        try:
            if not self._is_alarm:
                return
            back_color = (self._current_r, self._current_g, self._current_b)
            screen.fill(back_color)
            for block in blocks:
                block.update_display(True, screen, size, self._fore_color, back_color, current_time)

            (self._current_r, self._step_r) = self._calculate_color_part(
                self._start_r,
                self._stop_r,
                self._step_r,
                self._current_r)
            (self._current_g, self._step_g) = self._calculate_color_part(
                self._start_g,
                self._stop_g,
                self._step_g,
                self._current_g)
            (self._current_b, self._step_b) = self._calculate_color_part(
                self._start_b,
                self._stop_b,
                self._step_b,
                self._current_b)

        except Exception as ex:
            self._logger.exception(ex)

    def init_draw(self):
        super(BlockAlarmRise, self).init_draw()
        (_, background_color, _, _) = self._setting.get_curret_setting()
        self._start_r = background_color[0]
        self._start_g = background_color[1]
        self._start_b = background_color[2]
        self._stop_r = self._back_color[0]
        self._stop_g = self._back_color[1]
        self._stop_b = self._back_color[2]
        self._step_r = (self._stop_r - self._start_r) / 20
        self._step_g = (self._stop_g - self._start_g) / 20
        self._step_b = (self._stop_b - self._start_b) / 20
        self._current_r = self._start_r
        self._current_g = self._start_g
        self._current_b = self._start_b

    def _calculate_color_part(self, start, stop, step, current):
        current += step
        if current > stop:
            step = -step
            current += step
        if current < start:
            step = -step
            current += step
        return (current, step)
