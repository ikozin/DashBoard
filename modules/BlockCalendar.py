import configparser 
import pygame
import pygame.locals
from datetime import date

from exceptions import ExceptionFormat, ExceptionNotFound
from modules.BlockBase import BlockBase

BLOCK_CALENDAR_DISPLAY_FORMAT = "%a %d %B %Y"

class BlockCalendar(BlockBase):
    """description of class"""

    def __init__(self, logger, setting):
        """Initializes (declare internal variables)"""
        super(BlockCalendar, self).__init__(logger, setting)
        self._font = None
        self._pos = None


    def init(self, fileName):
        """Initializes (initialize internal variables)"""
        config = configparser.ConfigParser()
        config.read(fileName, "utf-8")
        section = config["CalendarBlock"]

        fontSize = section.getint("FontSize")
        fontName = section.get("FontName")
        isBold = section.getboolean("FontBold")
        isItalic = section.getboolean("FontItalic")
        self._pos = section.getint("Position")

        if fontSize is None:  raise ExceptionNotFound(section.name, "FontSize")
        if fontName is None:  raise ExceptionNotFound(section.name, "FontName")
        if isBold   is None:  raise ExceptionNotFound(section.name, "FontBold")
        if isItalic is None:  raise ExceptionNotFound(section.name, "FontItalic")
        if self._pos is None: raise ExceptionNotFound(section.name, "Position")

        self._font = pygame.font.SysFont(fontName, fontSize, isBold, isItalic)


    def updateDisplay(self, isOnline, screen, size, foreColor, backColor):
        try:
            if not isOnline: return

            self._text = date.today().strftime(BLOCK_CALENDAR_DISPLAY_FORMAT)
            sz = self._font.size(self._text)
            x = (size[0] - sz[0]) >> 1
            y = self._pos
            surf = self._font.render(self._text, True, foreColor, backColor)
            screen.blit(surf, (x, y))
        except Exception as ex:
            self._logger.exception(ex)


