import pygame
import pygame.locals

from typing import Dict
from datetime import datetime
from exceptions import ExceptionFormat, ExceptionNotFound
from modules.BlockBase import BlockBase
from logging import Logger
from setting import Setting


class BlockTime(BlockBase):
    """description of class"""

    def __init__(self, logger: Logger, setting: Setting):
        """Initializes (declare internal variables)"""
        super(BlockTime, self).__init__(logger, setting)

        self._format = ""
        self._format_time = ""
        self._font = None
        self._pos = None
        self._align_x = ""
        self._align_y = ""
        self._time = None

    def init(self, mod_list: Dict[str, BlockBase]) -> None:
        """Initializes (initialize internal variables)"""
        # Загружаем настройки
        section = self._setting.configuration["TimeBlock"]

        self._format = section.get("FormatText")

        self._format_time = section.get("Text")
        font_name = section.get("FontName")
        font_size = section.getint("FontSize")
        is_bold = section.getboolean("FontBold")
        is_italic = section.getboolean("FontItalic")
        self._pos = self._get_tuple(section.get("Pos"))
        self._align_x = section.get("AlignX")
        self._align_y = section.get("AlignY")

        if self._format is None:
            raise ExceptionNotFound(section.name, "FormatText")
        if self._format_time is None:
            raise ExceptionNotFound(section.name, "Text")
        if font_name is None:
            raise ExceptionNotFound(section.name, "FontName")
        if font_size is None:
            raise ExceptionNotFound(section.name, "FontSize")
        if is_bold is None:
            raise ExceptionNotFound(section.name, "FontBold")
        if is_italic is None:
            raise ExceptionNotFound(section.name, "FontItalic")
        if self._pos is None:
            raise ExceptionNotFound(section.name, "Pos")
        if self._align_x is None:
            raise ExceptionNotFound(section.name, "AlignX")
        if self._align_y is None:
            raise ExceptionNotFound(section.name, "AlignY")

        if len(self._pos) != 2:
            raise ExceptionFormat(section.name, "Pos")

        self._font = pygame.font.SysFont(font_name, font_size, is_bold, is_italic)
        self.update_info(True)

    def update_display(self, is_online: bool, screen, size, fore_color, back_color, current_time) -> None:
        try:
            if not is_online:
                return
            text = self._format_time.format(current_time)
            text_size = self._font.size(text)
            surf = self._font.render(text, True, fore_color, back_color)
            screen.blit(surf, self.calc_position(text_size, self._pos, self._align_x, self._align_y))
            self._time = current_time
        except Exception as ex:
            self._logger.exception(ex)

    def execute(self, *args) -> None:
        if self._time is None:
            self._time = datetime.now()
        self._text = self._format.format(self._time)
        self._time = None

    def get_text(self) -> str:
        self.execute()
        return self._text
