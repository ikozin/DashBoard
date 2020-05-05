from typing import Dict
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

    def init(self, mod_list: Dict[str, BlockBase]) -> None:
        """Initializes (initialize internal variables)"""
        # Загружаем настройки
        section = self._setting.configuration["VolumeBlock"]

        self._volume = section.getint("Volume")

        if self._volume is None:
            raise ExceptionNotFound(section.name, "Volume")

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

    def execute(self, *args) -> None:
        case = ""

        if len(args) == 1:
            case = args[0]

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

        if self._is_muted:
            pygame.mixer.music.set_volume(0)
        else:
            pygame.mixer.music.set_volume(self._volume / 100)
