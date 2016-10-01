import configparser 
import pygame
import pygame.locals
from datetime import date

from exceptions import ExceptionFormat, ExceptionNotFound
from modules.BlockBase import BlockBase


class BlockCalendar(BlockBase):
    """description of class"""

    def __init__(self, logger, setting):
        """Initializes (declare internal variables)"""
        super(BlockCalendar, self).__init__(logger, setting)
        self._daysLong = ["первое", "второе", "третье", "четвертое", "пятое", "шестое", "седьмое", "восьмое", "девятое", "десятое", "одиннадцатое", "двенадцатое", "тринадцатое", "четырнадцатое", "пятнадцатое", "шестнадцатое", "семнадцатое", "восенадцатое", "девятнадцатое", "двадцатое", "двадцать первое", "двадцать второе", "двадцать третье", "двадцать четвертое", "двадцать пятое", "двадцать шестое", "двадцать седьмое", "двадцать восьмое", "двадцать девятое", "тридцатое", "тридцать первое", "тридцать второе"]
        self._months   = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря"]
        self._weekDayShot = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        self._weekDayLong = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
        self._font = None
        self._pos = None


    def init(self, fileName, isOnline, modList):
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

        self.updateInfo(isOnline)


    def updateDisplay(self, isOnline, screen, size, foreColor, backColor):
        try:
            if not isOnline: return
            time = date.today()
            text = "{0} {1} {2} {3}".format(self._weekDayShot[time.weekday()], time.day, self._months[time.month-1], time.year)
            sz = self._font.size(text)
            x = (size[0] - sz[0]) >> 1
            y = self._pos
            surf = self._font.render(text, True, foreColor, backColor)
            screen.blit(surf, (x, y))
        except Exception as ex:
            self._logger.exception(ex)


    def getText(self):
        """ """
        time = date.today()
        self._text = "{0}, {1} {2} {3} год".format(self._weekDayLong[time.weekday()], self._daysLong[time.day-1], self._months[time.month-1], time.year)
        return self._text
