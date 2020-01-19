import urllib.request as request
import urllib.parse as parse
import xml.etree.ElementTree as ET
import pygame
import pygame.locals

from urllib.error import URLError
from exceptions import ExceptionNotFound
from modules.BlockMinuteBase import BlockMinuteBase
from logging import Logger
from setting import Setting

BLOCK_YANDEX_NEWS_CONFIG_EXCEPTION = "Ошибка конфигурации! В секции [YandexNewsBlock] пропущен параметр {0}"


class BlockYandexNews(BlockMinuteBase):
    """description of class"""

    def __init__(self, logger: Logger, setting: Setting):
        """Initializes (declare internal variables)"""
        super(BlockYandexNews, self).__init__(logger, setting)
        self._url = None
        self._indent = None
        self._pos = None
        self._length = None
        self._font = None
        self._news = []

    def init(self, mod_list) -> None:
        """Initializes (initialize internal variables)"""
        # Загружаем настройки
        section = self._setting.configuration["YandexNewsBlock"]

        self._url = section.get("Url")
        self._indent = section.getint("Indent")
        self._pos = section.getint("Position")
        self._length = section.getint("Rows")
        time = section.getint("UpdateTime")

        font_name = section.get("FontName")
        font_size = section.getint("FontSize")
        is_bold = section.getboolean("FontBold")
        is_italic = section.getboolean("FontItalic")

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

        if font_name is None:
            raise ExceptionNotFound(section.name, "FontName")
        if font_size is None:
            raise ExceptionNotFound(section.name, "FontSize")
        if is_bold is None:
            raise ExceptionNotFound(section.name, "FontBold")
        if is_italic is None:
            raise ExceptionNotFound(section.name, "FontItalic")

        self._font = pygame.font.SysFont(font_name, font_size, is_bold, is_italic)

        self.update_info(True)
        self.set_time(time)

    def update_info(self, is_online):
        try:
            if not is_online:
                return
            self.execute()
        except URLError as ex:
            self._logger.exception(ex)
        except Exception as ex:
            self._logger.exception(ex)

    def update_display(self, is_online: bool, screen, size, fore_color, back_color, current_time) -> None:
        try:
            if not is_online:
                return
            if not self._news:
                return

            text_y = self._pos
            for text in self._news:
                text_size = self._font.size(text)
                text_x = (size[0] - min(size[0], text_size[0])) >> 1
                surf = self._font.render(text, True, fore_color, back_color)
                screen.blit(surf, (text_x, text_y))
                text_y += text_size[1] + self._indent
        except Exception as ex:
            self._logger.exception(ex)

    def execute(self, *args) -> None:
        self._news = [line for (index, line) in enumerate(self.__get_newsblock(self._url)) if index < self._length]
        self._text = "Новости от Яндекса. %s" % '.'.join(self._news) if self._news else None

    def __get_newsblock(self, url):
        news = []
        data = request.urlopen(url).read()
        root = ET.fromstring(data)
        for node in root.findall("./channel/item/title"):
            news.append(parse.unquote(node.text))
        return news
