import configparser 
import pygame
import pygame.locals
from datetime import date

from block_base import BlockBase
from setting import TEXT_EXCEPTION_NOT_FOUND

BLOCK_CALENDAR_DISPLAY_FORMAT = "%a %d %B %Y"

class BlockCalendar(BlockBase):
    """description of class"""

    def __init__(self, logger):
        "Ininitializes"
        super(BlockCalendar, self).__init__(logger)
        self._font = None
        self._pos = None


    def init(self, fileName):
        config = configparser.ConfigParser()
        config.read(fileName, encoding="utf-8")
        section = config["CalendarBlock"]

        fontSize = section.getint("FontSize")
        fontName = section.get("FontName")
        self._pos = section.getint("Position")
        if not fontSize:  raise Exception(TEXT_EXCEPTION_NOT_FOUND.format("CalendarBlock", "FontSize"))
        if not fontName:  raise Exception(TEXT_EXCEPTION_NOT_FOUND.format("CalendarBlock", "FontName"))
        if not self._pos: raise Exception(TEXT_EXCEPTION_NOT_FOUND.format("CalendarBlock", "Position"))
        self._font = pygame.font.SysFont(fontName, fontSize)


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


