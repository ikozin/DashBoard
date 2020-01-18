from exceptions import ExceptionNotFound
import pygame
import pygame.locals
from modules.BlockBase import BlockBase


class BlockBme280(BlockBase):
    """description of class"""

    def __init__(self, logger, setting):
        """Initializes (declare internal variables)"""
        super(BlockBme280, self).__init__(logger, setting)
        self._font = None
        self._pos = None

    def init(self, mod_list):
        """Initializes (initialize internal variables)"""
        # Загружаем настройки
        section = self._setting.configuration["BME280Block"]

        font_name = section.get("FontName")
        font_size = section.getint("FontSize")
        is_bold = section.getboolean("FontBold")
        is_italic = section.getboolean("FontItalic")
        self._pos = section.getint("Position")

        if font_name is None:
            raise ExceptionNotFound(section.name, "FontName")
        if font_size is None:
            raise ExceptionNotFound(section.name, "FontSize")
        if is_bold is None:
            raise ExceptionNotFound(section.name, "FontBold")
        if is_italic is None:
            raise ExceptionNotFound(section.name, "FontItalic")
        if self._pos is None:
            raise ExceptionNotFound(section.name, "Position")

        self._font = pygame.font.SysFont(font_name, font_size, is_bold, is_italic)
        self.update_info(True)

    def update_display(self, is_online, screen, size, fore_color, back_color, current_time):
        try:
            if not is_online:
                return
        except Exception as ex:
            self._logger.exception(ex)

    def execute(self, *args):
        self._text = ""

    def get_text(self):
        self.execute()
        return self._text

