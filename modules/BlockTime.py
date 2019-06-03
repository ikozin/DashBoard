from datetime import datetime
from exceptions import ExceptionNotFound
import pygame
import pygame.locals
from modules.BlockBase import BlockBase

BLOCK_TIME_DISPLAY_FORMAT = "{:%H:%M}"
BLOCK_TIME_TIME_TEXT = "Московское время {:%H:%M}"


class BlockTime(BlockBase):
    """description of class"""

    def __init__(self, logger, setting):
        """Initializes (declare internal variables)"""
        super(BlockTime, self).__init__(logger, setting)
        self._font = None
        self._time = None

    def init(self, mod_list):
        """Initializes (initialize internal variables)"""
        # Загружаем настройки
        section = self._setting.Configuration["TimeBlock"]

        font_name = section.get("FontName")
        font_size = section.getint("FontSize")
        is_bold = section.getboolean("FontBold")
        is_italic = section.getboolean("FontItalic")

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

    def update_display(self, is_online, screen, size, fore_color, back_color, current_time):
        try:
            if not is_online:
                return
            text = BLOCK_TIME_DISPLAY_FORMAT.format(current_time)
            text_size = self._font.size(text)
            text_x = (size[0] - text_size[0]) >> 1
            text_y = (size[1] - text_size[1]) >> 1
            surf = self._font.render(text, True, fore_color, back_color)
            screen.blit(surf, (text_x, text_y))
            self._time = current_time
        except Exception as ex:
            self._logger.exception(ex)

    def execute(self, *args):
        if self._time is None:
            self._time = datetime.now()
        self._text = BLOCK_TIME_TIME_TEXT.format(self._time)
        self._time = None

    def get_text(self):
        self.execute()
        return self._text
