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
        self._temperature_font = None
        self._humidity_font = None
        self._pressure_font = None
        self._temperature_text = ""
        self._humidity_text = ""
        self._pressure_text = ""
        self._temperature_pos = None
        self._humidity_pos = None
        self._pressure_pos = None
        self._temperature_align_x = ""
        self._temperature_align_y = ""
        self._humidity_align_x = ""
        self._humidity_align_y = ""
        self._pressure_align_x = ""
        self._pressure_align_y = ""

        self._format = ""

    def init(self, mod_list: Dict[str, BlockBase]) -> None:
        """Initializes (initialize internal variables)"""
        # Загружаем настройки
        section = self._setting.configuration["BME280Block"]

        self._address = section.getint("Address")
        self._format = section.get("FormatText")

        self._temperature_text = section.get("TemperatureText")
        temperature_font_name = section.get("TemperatureFontName")
        temperature_font_size = section.getint("TemperatureFontSize")
        temperature_is_bold = section.getboolean("TemperatureFontBold")
        temperature_is_italic = section.getboolean("TemperatureFontItalic")
        self._temperature_pos = self._get_tuple(section.get("TemperaturePos"))
        self._temperature_align_x = section.get("TemperatureAlignX")
        self._temperature_align_y = section.get("TemperatureAlignY")

        self._humidity_text = section.get("HumidityText")
        humidity_font_name = section.get("HumidityFontName")
        humidity_font_size = section.getint("HumidityFontSize")
        humidity_is_bold = section.getboolean("HumidityFontBold")
        humidity_is_italic = section.getboolean("HumidityFontItalic")
        self._humidity_pos = self._get_tuple(section.get("HumidityPos"))
        self._humidity_align_x = section.get("HumidityAlignX")
        self._humidity_align_y = section.get("HumidityAlignY")

        self._pressure_text = section.get("PressureText")
        pressure_font_name = section.get("PressureFontName")
        pressure_font_size = section.getint("PressureFontSize")
        pressure_is_bold = section.getboolean("PressureFontBold")
        pressure_is_italic = section.getboolean("PressureFontItalic")
        self._pressure_pos = self._get_tuple(section.get("PressurePos"))
        self._pressure_align_x = section.get("PressureAlignX")
        self._pressure_align_y = section.get("PressureAlignY")
        
        if self._address is None:
            raise ExceptionNotFound(section.name, "Address")
        if self._format is None:
            raise ExceptionNotFound(section.name, "FormatText")

        if self._temperature_text is None:
            raise ExceptionNotFound(section.name, "TemperatureText")
        if temperature_font_name is None:
            raise ExceptionNotFound(section.name, "TemperatureFontName")
        if temperature_font_size is None:
            raise ExceptionNotFound(section.name, "TemperatureFontSize")
        if temperature_is_bold is None:
            raise ExceptionNotFound(section.name, "TemperatureFontBold")
        if temperature_is_italic is None:
            raise ExceptionNotFound(section.name, "TemperatureFontItalic")
        if self._temperature_pos is None:
            raise ExceptionNotFound(section.name, "TemperaturePos")

        if self._humidity_text is None:
            raise ExceptionNotFound(section.name, "HumidityText")
        if humidity_font_name is None:
            raise ExceptionNotFound(section.name, "HumidityFontName")
        if humidity_font_size is None:
            raise ExceptionNotFound(section.name, "HumidityFontSize")
        if humidity_is_bold is None:
            raise ExceptionNotFound(section.name, "HumidityFontBold")
        if humidity_is_italic is None:
            raise ExceptionNotFound(section.name, "HumidityFontItalic")
        if self._humidity_pos is None:
            raise ExceptionNotFound(section.name, "HumidityPos")

        if self._pressure_text is None:
            raise ExceptionNotFound(section.name, "PressureText")
        if pressure_font_name is None:
            raise ExceptionNotFound(section.name, "PressureFontName")
        if pressure_font_size is None:
            raise ExceptionNotFound(section.name, "PressureFontSize")
        if pressure_is_bold is None:
            raise ExceptionNotFound(section.name, "PressureFontBold")
        if pressure_is_italic is None:
            raise ExceptionNotFound(section.name, "PressureFontItalic")
        if self._pressure_pos is None:
            raise ExceptionNotFound(section.name, "PressurePos")

        if len(self._temperature_pos) != 2:
            raise ExceptionFormat(section.name, "TemperaturePos")
        if len(self._humidity_pos) != 2:
            raise ExceptionFormat(section.name, "HumidityPos")
        if len(self._pressure_pos) != 2:
            raise ExceptionFormat(section.name, "PressurePos")

        self._temperature_font = pygame.font.SysFont(temperature_font_name, temperature_font_size, temperature_is_bold, temperature_is_italic)
        self._humidity_font = pygame.font.SysFont(humidity_font_name, humidity_font_size, humidity_is_bold, humidity_is_italic)
        self._pressure_font = pygame.font.SysFont(pressure_font_name, pressure_font_size, pressure_is_bold, pressure_is_italic)

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
                text_size = self._temperature_font.size(text)
                surf = self._temperature_font.render(text, True, fore_color, back_color)
                screen.blit(surf, self.calc_position(text_size, self._temperature_pos, self._temperature_align_x, self._temperature_align_y))
            if len(self._humidity_text) > 0:
                text = self._humidity_text.format(self._temperature, self._humidity, self._pressure)
                text_size = self._humidity_font.size(text)
                surf = self._humidity_font.render(text, True, fore_color, back_color)
                screen.blit(surf, self.calc_position(text_size, self._humidity_pos, self._humidity_align_x, self._humidity_align_y))
            if len(self._pressure_text) > 0:
                text = self._pressure_text.format(self._temperature, self._humidity, self._pressure)
                text_size = self._pressure_font.size(text)
                surf = self._pressure_font.render(text, True, fore_color, back_color)
                screen.blit(surf, self.calc_position(text_size, self._pressure_pos, self._pressure_align_x, self._pressure_align_y))
        except Exception as ex:
            self._logger.exception(ex)

    def execute(self, *args) -> None:
        (self._temperature, self._pressure, self._humidity) = self._device.read()
        self._text = self._format.format(self._temperature, self._humidity, self._pressure)

    def get_text(self) -> str:
        self.execute()
        return self._text
