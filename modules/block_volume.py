from typing import Dict, Any
from datetime import datetime
from exceptions import ExceptionNotFound
from modules.BlockBase import BlockBase
from logging import Logger
from setting import Setting

import pygame
import pygame.locals


class BlockVolume(BlockBase):
    """description of class"""

    def __init__(self, logger: Logger, setting: Setting):
        """Initializes (declare internal variables)"""
        super(BlockVolume, self).__init__(logger, setting)
        self._blocks = []
        self._volume = 0
        self._is_muted = False
        self._font = None
        self._pos = None
        self._align_x = ""
        self._align_y = ""
        self._start_time = None

    def init(self, mod_list: Dict[str, BlockBase]) -> None:
        """Initializes (initialize internal variables)"""
        # Загружаем настройки
        section = self._setting.configuration["VolumeBlock"]

        self._volume = section.getint("Volume")

        font_name = section.get("FontName")
        font_size = section.getint("FontSize")
        is_bold = section.getboolean("FontBold")
        is_italic = section.getboolean("FontItalic")
        self._pos = self._get_tuple(section.get("Pos"))
        self._align_x = section.get("AlignX")
        self._align_y = section.get("AlignY")

        if self._volume is None:
            raise ExceptionNotFound(section.name, "Volume")
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

        self._font = pygame.font.SysFont(font_name, font_size, is_bold, is_italic)
        self.execute()

    def procced_event(self, event, is_online: bool) -> None:
        try:
            if (event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_KP_PLUS):
                self.execute("+")
            if (event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_KP_MINUS):
                self.execute("-")
            if (event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_KP_DIVIDE):
                self.execute("off")
            if (event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_KP_MULTIPLY):
                self.execute("on")
        except Exception as ex:
            self._logger.exception(ex)

    def execute(self, *args) -> Any:
        case = ""

        if len(args) == 1:
            case = str(args[0])

        if case == "+":
            self._volume = self._volume + 5
            if self._volume > 100:
                self._volume = 100

        elif case == "-":
            self._volume = self._volume - 5
            if self._volume < 0:
                self._volume = 0

        elif case == "off":
            self._is_muted = True

        elif case == "on":
            self._is_muted = False

        elif len(case):
            self._volume = int(case)

        if self._is_muted:
            pygame.mixer.music.set_volume(0)
        else:
            pygame.mixer.music.set_volume(self._volume / 100)

        self._start_time = datetime.now()
        return self._volume

    def update_display(self, is_online: bool, screen, size, fore_color, back_color, current_time) -> None:
        try:
            if not is_online:
                return
            if not self._start_time:
                return
            delta = current_time - self._start_time
            if delta.total_seconds() > 3:
                self._start_time = None
            text = "{0}".format(self._volume)
            text_size = self._font.size(text)
            surf = self._font.render(text, True, (0, 255, 0), back_color)
            screen.blit(surf, self.calc_position(text_size, self._pos, self._align_x, self._align_y))
            self._time = current_time
        except Exception as ex:
            self._logger.exception(ex)
