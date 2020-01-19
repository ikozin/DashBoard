import pygame
import pygame.locals

from datetime import datetime
from exceptions import ExceptionNotFound
from modules.BlockBase import BlockBase
from logging import Logger
from setting import Setting


class BlockCalendar(BlockBase):
    """description of class"""

    def __init__(self, logger: Logger, setting: Setting):
        """Initializes (declare internal variables)"""
        super(BlockCalendar, self).__init__(logger, setting)
        self._days_long = [
            "первое",
            "второе",
            "третье",
            "четвертое",
            "пятое",
            "шестое",
            "седьмое",
            "восьмое",
            "девятое",
            "десятое",
            "одиннадцатое",
            "двенадцатое",
            "тринадцатое",
            "четырнадцатое",
            "пятнадцатое",
            "шестнадцатое",
            "семнадцатое",
            "восемнадцатое",
            "девятнадцатое",
            "двадцатое",
            "двадцать первое",
            "двадцать второе",
            "двадцать третье",
            "двадцать четвертое",
            "двадцать пятое",
            "двадцать шестое",
            "двадцать седьмое",
            "двадцать восьмое",
            "двадцать девятое",
            "тридцатое",
            "тридцать первое",
            "тридцать второе"]
        self._months = [
            "января",
            "февраля",
            "марта",
            "апреля",
            "мая",
            "июня",
            "июля",
            "августа",
            "сентября",
            "октября",
            "ноября",
            "декабря"]
        self._weekday_shot = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        self._weekday_long = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
        self._font = None
        self._pos = None
        self._time = None

    def init(self, mod_list) -> None:
        """Initializes (initialize internal variables)"""
        # Загружаем настройки
        section = self._setting.configuration["CalendarBlock"]

        font_name = section.get("FontName")
        font_size = section.getint("FontSize")
        is_bold = section.getboolean("FontBold")
        is_italic = section.getboolean("FontItalic")
        self._pos = section.getint("Position")

        if font_name is None:
            raise ExceptionNotFound(section.name, "FontName")
        if font_size is None:
            raise ExceptionNotFound(section.name, "FontSize")
        if is_bold is None:
            raise ExceptionNotFound(section.name, "FontBold")
        if is_italic is None:
            raise ExceptionNotFound(section.name, "FontItalic")
        if self._pos is None:
            raise ExceptionNotFound(section.name, "Position")

        self._font = pygame.font.SysFont(font_name, font_size, is_bold, is_italic)
        self.update_info(True)

    def update_display(self, is_online: bool, screen, size, fore_color, back_color, current_time) -> None:
        try:
            self._time = current_time
            if not is_online:
                return
            text = "{0} {1} {2} {3}".format(
                self._weekday_shot[self._time.weekday()],
                self._time.day,
                self._months[self._time.month-1],
                self._time.year)
            text_size = self._font.size(text)
            text_x = (size[0] - text_size[0]) >> 1
            text_y = self._pos
            surf = self._font.render(text, True, fore_color, back_color)
            screen.blit(surf, (text_x, text_y))
        except Exception as ex:
            self._logger.exception(ex)

    def execute(self, *args) -> None:
        if self._time is None:
            self._time = datetime.now()
        self._text = "{0}, {1} {2} {3} год".format(
            self._weekday_long[self._time.weekday()],
            self._days_long[self._time.day-1],
            self._months[self._time.month-1],
            self._time.year)
        self._time = None

    def get_text(self) -> str:
        self.execute()
        return self._text
