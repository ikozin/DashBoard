import pygame
import pygame.locals

from typing import Dict
from exceptions import ExceptionFormat, ExceptionNotFound
from modules.BlockBase import BlockBase
from modules.hal.bme280_base import Bme280_Base

from logging import Logger
from setting import Setting


class BlockBme280(BlockBase):
    """description of class"""

    def __init__(self, logger: Logger, setting: Setting, hal: Bme280_Base):
        """Initializes (declare internal variables)"""
        super(BlockBme280, self).__init__(logger, setting)

        self._hal = hal
        self._address = 0
        self._temperature = None
        self._pressure = None
        self._humidity = None
        self._font = None
        self._temperature_text = None
        self._humidity_text = None
        self._pressure_text = None
        self._temperature_pos = None
        self._humidity_pos = None
        self._pressure_pos = None
        self._format = None

    def init(self, mod_list: Dict[str, BlockBase]) -> None:
        """Initializes (initialize internal variables)"""
        # Загружаем настройки
        section = self._setting.configuration["BME280Block"]

        self._address = section.getint("Address")
        font_name = section.get("FontName")
        font_size = section.getint("FontSize")
        is_bold = section.getboolean("FontBold")
        is_italic = section.getboolean("FontItalic")
        self._temperature_text = section.get("TemperatureText")
        self._humidity_text = section.get("HumidityText")
        self._pressure_text = section.get("PressureText")
        self._temperature_pos = self._get_tuple(section.get("TemperaturePos"))
        self._humidity_pos = self._get_tuple(section.get("HumidityPos"))
        self._pressure_pos = self._get_tuple(section.get("PressurePos"))
        self._format = section.get("FormatText")

        if self._address is None:
            raise ExceptionNotFound(section.name, "Address")
        if font_name is None:
            raise ExceptionNotFound(section.name, "FontName")
        if font_size is None:
            raise ExceptionNotFound(section.name, "FontSize")
        if is_bold is None:
            raise ExceptionNotFound(section.name, "FontBold")
        if is_italic is None:
            raise ExceptionNotFound(section.name, "FontItalic")
        if self._temperature_text is None:
            raise ExceptionNotFound(section.name, "TemperatureText")
        if self._humidity_text is None:
            raise ExceptionNotFound(section.name, "HumidityText")
        if self._pressure_text is None:
            raise ExceptionNotFound(section.name, "PressureText")
        if self._temperature_pos is None:
            raise ExceptionNotFound(section.name, "TemperaturePos")
        if self._humidity_pos is None:
            raise ExceptionNotFound(section.name, "HumidityPos")
        if self._pressure_pos is None:
            raise ExceptionNotFound(section.name, "PressurePos")
        if self._format is None:
            raise ExceptionNotFound(section.name, "FormatText")

        if len(self._temperature_pos) != 2:
            raise ExceptionFormat(section.name, "TemperaturePos")
        if len(self._humidity_pos) != 2:
            raise ExceptionFormat(section.name, "HumidityPos")
        if len(self._pressure_pos) != 2:
            raise ExceptionFormat(section.name, "PressurePos")

        self._font = pygame.font.SysFont(font_name, font_size, is_bold, is_italic)

        self._device = self._hal(self._logger, self._address)
        self.update_info(True)

    def update_info(self, is_online: bool) -> None:
        if not is_online:
            return
        self.execute()

    def update_display(self, is_online: bool, screen, size, fore_color, back_color, current_time) -> None:
        try:
            self._time = current_time
            if not is_online:
                return
            if len(self._temperature_text) > 0:
                text = self._temperature_text.format(self._temperature, self._humidity, self._pressure)
                surf = self._font.render(text, True, fore_color, back_color)
                screen.blit(surf, self._temperature_pos)
            if len(self._humidity_text) > 0:
                text = self._humidity_text.format(self._temperature, self._humidity, self._pressure)
                surf = self._font.render(text, True, fore_color, back_color)
                screen.blit(surf, self._humidity_pos)
            if len(self._pressure_text) > 0:
                text = self._pressure_text.format(self._temperature, self._humidity, self._pressure)
                surf = self._font.render(text, True, fore_color, back_color)
                screen.blit(surf, self._pressure_pos)
        except Exception as ex:
            self._logger.exception(ex)

    def execute(self, *args) -> None:
        (self._temperature, self._pressure, self._humidity) = self._device.read()
        self._text = self._format.format(self._temperature, self._humidity, self._pressure)

    def get_text(self) -> str:
        self.execute()
        return self._text
