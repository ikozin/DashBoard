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
        "Ininitializes"
        super(BlockYandexNews, self).__init__(logger)
        self._url = None
        self._fontSize = None
        self._fontName = None
        self._line = None
        self._pos = None
        self._length = None
        self._time = None
        self._news = []


    def init(self, fileName):
        # Загружаем настройки
        config = configparser.ConfigParser()
        config.read(fileName, encoding="utf-8")
        section = config["YandexNewsBlock"]
        self._url = section.get("Url")
        self._fontSize = section.getint("FontSize")
        self._fontName = section.get("FontName")
        self._line = section.getint("Line")
        self._pos = section.getint("Position")
        self._length = section.getint("Length")
        self._time = section.getint("UpdateTime")
        if not self._url:      raise Exception(TEXT_EXCEPTION_NOT_FOUND.format("YandexNewsBlock", "Url"))
        if not self._fontSize: raise Exception(TEXT_EXCEPTION_NOT_FOUND.format("YandexNewsBlock", "FontSize"))
        if not self._fontName: raise Exception(TEXT_EXCEPTION_NOT_FOUND.format("YandexNewsBlock", "FontName"))
        if not self._line:     raise Exception(TEXT_EXCEPTION_NOT_FOUND.format("YandexNewsBlock", "Line"))
        if not self._pos:      raise Exception(TEXT_EXCEPTION_NOT_FOUND.format("YandexNewsBlock", "Position"))
        if not self._length:   raise Exception(TEXT_EXCEPTION_NOT_FOUND.format("YandexNewsBlock", "Length"))
        if not self._time:     raise Exception(TEXT_EXCEPTION_NOT_FOUND.format("YandexNewsBlock", "UpdateTime"))
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
            font = pygame.font.SysFont(self._fontName, self._fontSize)
            for text in self._news:
                sz = font.size(text)
                x = (size[0] - min(size[0], sz[0])) >> 1
                surf = font.render(text, True, foreColor, backColor)
                screen.blit(surf, (x, y))
                y += sz[1] + self._line
        except Exception as ex:
            self._logger.exception(ex)


    def __get_newsblock(self, url):
        news = []
        data = request.urlopen(url).read()
        root = ET.fromstring(data)
        for node in root.findall("./channel/item/title"):
            news.append(parse.unquote(node.text))
        return news
        
