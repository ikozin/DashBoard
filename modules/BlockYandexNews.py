import urllib.request as request
import urllib.parse as parse
import xml.etree.ElementTree as ET
import pygame
import pygame.locals

from exceptions import ExceptionNotFound
from modules.BlockMinuteBase import BlockMinuteBase

BLOCK_YANDEX_NEWS_CONFIG_EXCEPTION = "Ошибка конфигурации! В секции [YandexNewsBlock] пропущен параметр {0}"


class BlockYandexNews(BlockMinuteBase):
    """description of class"""

    def __init__(self, logger, setting):
        """Initializes (declare internal variables)"""
        super(BlockYandexNews, self).__init__(logger, setting)
        self._url = None
        self._indent = None
        self._pos = None
        self._length = None
        self._font = None
        self._news = []

    def init(self, modList):
        """Initializes (initialize internal variables)"""
        # Загружаем настройки
        section = self._setting.Configuration["YandexNewsBlock"]

        self._url = section.get("Url")
        self._indent = section.getint("Indent")
        self._pos = section.getint("Position")
        self._length = section.getint("Rows")
        time = section.getint("UpdateTime")

        fontName = section.get("FontName")
        fontSize = section.getint("FontSize")
        isBold = section.getboolean("FontBold")
        isItalic = section.getboolean("FontItalic")

        if self._url is None:
            raise ExceptionNotFound(section.name, "Url")
        if self._indent is None:
            raise ExceptionNotFound(section.name, "Indent")
        if self._pos is None:
            raise ExceptionNotFound(section.name, "Position")
        if self._length is None:
            raise ExceptionNotFound(section.name, "Rows")
        if time is None:
            raise ExceptionNotFound(section.name, "UpdateTime")

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
        self.setTime(time)

    def updateInfo(self, isOnline):
        try:
            if not isOnline:
                return
            self.execute()
        except Exception as ex:
            self._logger.exception(ex)

    def updateDisplay(self, isOnline, screen, size, foreColor, backColor, current_time):
        try:
            if not isOnline:
                return
            if not self._news:
                return

            y = self._pos
            for text in self._news:
                sz = self._font.size(text)
                x = (size[0] - min(size[0], sz[0])) >> 1
                surf = self._font.render(text, True, foreColor, backColor)
                screen.blit(surf, (x, y))
                y += sz[1] + self._indent
        except Exception as ex:
            self._logger.exception(ex)

    def execute(self, *args):
        self._news = [line for (index, line) in enumerate(self.__get_newsblock(self._url)) if index < self._length]
        self._text = "Новости от Яндекса. %s" % '.'.join(self._news) if self._news else None

    def __get_newsblock(self, url):
        news = []
        data = request.urlopen(url).read()
        root = ET.fromstring(data)
        for node in root.findall("./channel/item/title"):
            news.append(parse.unquote(node.text))
        return news
