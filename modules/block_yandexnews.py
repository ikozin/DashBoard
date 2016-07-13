import configparser 
import urllib.request as request
import urllib.parse as parse
import xml.etree.ElementTree as ET
import pygame
import pygame.locals

from block_base import BlockBase
from setting import TEXT_EXCEPTION_NOT_FOUND

BLOCK_YANDEX_NEWS_CONFIG_EXCEPTION = "Ошибка конфигурации! В секции [YandexNewsBlock] пропущен параметр {0}"
BLOCK_YANDEX_NEWS_UPDATE_EVENT = (pygame.locals.USEREVENT + 2)

class BlockYandexNews(BlockBase):
    """description of class"""
    
    def __init__(self, logger):
        """Initializes (declare internal variables)"""
        super(BlockYandexNews, self).__init__(logger)
        self._url = None
        self._indent = None
        self._pos = None
        self._length = None
        self._time = None
        self._font = None
        self._news = []


    def init(self, fileName):
        """Initializes (initialize internal variables)"""
        # Загружаем настройки
        config = configparser.ConfigParser()
        config.read(fileName, "utf-8")
        section = config["YandexNewsBlock"]

        self._url = section.get("Url")
        self._indent = section.getint("Indent")
        self._pos = section.getint("Position")
        self._length = section.getint("Rows")
        self._time = section.getint("UpdateTime")

        fontName = section.get("FontName")
        fontSize = section.getint("FontSize")
        isBold = section.getboolean("FontBold")
        isItalic = section.getboolean("FontItalic")

        if self._url is None:    raise Exception(TEXT_EXCEPTION_NOT_FOUND.format("YandexNewsBlock", "Url"))
        if self._indent is None:   raise Exception(TEXT_EXCEPTION_NOT_FOUND.format("YandexNewsBlock", "Indent"))
        if self._pos is None:    raise Exception(TEXT_EXCEPTION_NOT_FOUND.format("YandexNewsBlock", "Position"))
        if self._length is None: raise Exception(TEXT_EXCEPTION_NOT_FOUND.format("YandexNewsBlock", "Rows"))
        if self._time is None:   raise Exception(TEXT_EXCEPTION_NOT_FOUND.format("YandexNewsBlock", "UpdateTime"))

        if fontName is None: raise Exception(TEXT_EXCEPTION_NOT_FOUND.format("YandexNewsBlock", "FontName"))
        if fontSize is None: raise Exception(TEXT_EXCEPTION_NOT_FOUND.format("YandexNewsBlock", "FontSize"))
        if isBold   is None: raise Exception(TEXT_EXCEPTION_NOT_FOUND.format("YandexNewsBlock", "FontBold"))
        if isItalic is None: raise Exception(TEXT_EXCEPTION_NOT_FOUND.format("YandexNewsBlock", "FontItalic"))

        self._font = pygame.font.SysFont(fontName, fontSize, isBold, isItalic)

        pygame.time.set_timer(BLOCK_YANDEX_NEWS_UPDATE_EVENT, self._time * 60000)
       

    def proccedEvent(self, event, isOnline):
        if event.type == BLOCK_YANDEX_NEWS_UPDATE_EVENT:
            self.updateInfo(isOnline)


    def updateInfo(self, isOnline):
        try:
            if not isOnline: return
            
            self._news = [line for (index, line) in enumerate(self.__get_newsblock(self._url)) if index < self._length]
            self._text = "Новости от Яндекса. %s" % '.'.join(self._news)
        except Exception as ex:
            self._logger.exception(ex)
            self._news = []
            self._text = None


    def updateDisplay(self, isOnline, screen, size, foreColor, backColor):
        try:
            if not isOnline: return
            if not self._news: return

            y = self._pos
            for text in self._news:
                sz = self._font.size(text)
                x = (size[0] - min(size[0], sz[0])) >> 1
                surf = self._font.render(text, True, foreColor, backColor)
                screen.blit(surf, (x, y))
                y += sz[1] + self._indent
        except Exception as ex:
            self._logger.exception(ex)


    def __get_newsblock(self, url):
        news = []
        data = request.urlopen(url).read()
        root = ET.fromstring(data)
        for node in root.findall("./channel/item/title"):
            news.append(parse.unquote(node.text))
        return news
        
