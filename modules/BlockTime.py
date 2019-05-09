import configparser
import pygame
import pygame.locals

from datetime import datetime
from modules.BlockBase import BlockBase
from exceptions import ExceptionFormat, ExceptionNotFound

BLOCK_TIME_DISPLAY_FORMAT = "{:%H:%M}"
BLOCK_TIME_TIME_TEXT = "Московское время {:%H:%M}"


class BlockTime(BlockBase):
    """description of class"""

    def __init__(self, logger, setting):
        """Initializes (declare internal variables)"""
        super(BlockTime, self).__init__(logger, setting)
        self._font = None
        self._time = None

    def init(self, modList):
        """Initializes (initialize internal variables)"""
        # Загружаем настройки
        section = self._setting.Configuration["TimeBlock"]

        fontName = section.get("FontName")
        fontSize = section.getint("FontSize")
        isBold = section.getboolean("FontBold")
        isItalic = section.getboolean("FontItalic")

        if fontName is None:
            raise ExceptionNotFound(section.name, "FontName")
        if fontSize is None:
            raise ExceptionNotFound(section.name, "FontSize")
        if isBold is None:
            raise ExceptionNotFound(section.name, "FontBold")
        if isItalic is None:
            raise ExceptionNotFound(section.name, "FontItalic")

        self._font = pygame.font.SysFont(fontName, fontSize, isBold, isItalic)
        self.updateInfo(True)

    def updateDisplay(self, isOnline, screen, size, foreColor, backColor, current_time):
        try:
            if not isOnline:
                return
            text = BLOCK_TIME_DISPLAY_FORMAT.format(current_time)
            sz = self._font.size(text)
            x = (size[0] - sz[0]) >> 1
            y = (size[1] - sz[1]) >> 1
            surf = self._font.render(text, True, foreColor, backColor)
            screen.blit(surf, (x, y))
            self._time = current_time
        except Exception as ex:
            self._logger.exception(ex)

    def execute(self, *args):
        if self._time is None:
            self._time = datetime.now()
        self._text = BLOCK_TIME_TIME_TEXT.format(self._time)
        self._time = None

    def getText(self):
        self.execute()
        return self._text
