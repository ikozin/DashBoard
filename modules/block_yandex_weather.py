import os
import urllib.request as request
import xml.etree.ElementTree as ET
import pygame

from datetime import datetime, timedelta
from exceptions import ExceptionFormat, ExceptionNotFound
from modules.BlockMinuteBase import BlockMinuteBase
from logging import Logger

MIN_UPDATE_TIME = 600
WEATHER_FILE = "yandexweather_data.xml"
WEATHER_TEXT_FORMAT = "{0}, Температура {1:+.0f}°, Скорость ветра {2} метра в секунду, " \
    "Влажность {3}%, Давление {4} мм ртутного столба"
DETAILS_TEXT_FORMAT = "Ветер {0} м/с {1}\nВлажность {2}%\nДавление {3} мм"


class BlockYandexWeather(BlockMinuteBase):
    """description of class"""

    def __init__(self, logger: Logger, setting):
        """Initializes (declare internal variables)"""
        super(BlockYandexWeather, self).__init__(logger, setting)
        self._last_update = datetime.now() - timedelta(seconds=MIN_UPDATE_TIME + 1)

        self._folder = None
        self._region_id = None
        self._lat = None
        self._lon = None

        self._weather_type = None
        self._temperature = None
        self._humidity = None
        self._pressure = None
        self._wind_speed = None
        self._wind_direction = None
        self._weather_image = None

        self._icon_scale = None
        self._icon_pos = None
        self._weather_type_pos = None
        self._temperature_pos = None
        self._humidity_pos = None
        self._pressure_pos = None
        self._wind_pos = None

        self._weather_type_font = None
        self._temperature_font = None
        self._humidity_font = None
        self._pressure_font = None
        self._wind_font = None

    def init(self, mod_list) -> None:
        """Initializes (initialize internal variables)"""
        # Загружаем настройки
        section = self._setting.configuration["YandexWeatherBlock"]

        self._folder = section.get("Folder")
        time = section.getint("UpdateTime")
        self._region_id = section.getint("RegionId")
        self._lat = section.get("Lat")
        self._lon = section.get("Lon")

        self._icon_scale = self._get_tuple(section.get("IconScale"))
        self._icon_pos = self._get_tuple(section.get("IconPos"))
        self._weather_type_pos = self._get_tuple(section.get("WeatherTypePos"))
        self._temperature_pos = self._get_tuple(section.get("TemperaturePos"))
        self._humidity_pos = self._get_tuple(section.get("HumidityPos"))
        self._pressure_pos = self._get_tuple(section.get("PressurePos"))
        self._wind_pos = self._get_tuple(section.get("WindPos"))

        wt_name = section.get("WeatherTypeFontName")
        t_name = section.get("TemperatureFontName")
        h_name = section.get("HumidityFontName")
        p_name = section.get("PressureFontName")
        w_name = section.get("WindFontName")

        wt_size = section.getint("WeatherTypeFontSize")
        t_size = section.getint("TemperatureFontSize")
        h_size = section.getint("HumidityFontSize")
        p_size = section.getint("PressureFontSize")
        w_size = section.getint("WindFontSize")

        wt_bold = section.getboolean("WeatherTypeFontBold")
        t_bold = section.getboolean("TemperatureFontBold")
        h_bold = section.getboolean("HumidityFontBold")
        p_bold = section.getboolean("PressureFontBold")
        w_bold = section.getboolean("WindFontBold")

        wt_italic = section.getboolean("WeatherTypeFontItalic")
        t_italic = section.getboolean("TemperatureFontItalic")
        h_italic = section.getboolean("HumidityFontItalic")
        p_italic = section.getboolean("PressureFontItalic")
        w_italic = section.getboolean("WindFontItalic")

        if self._folder is None:
            raise ExceptionNotFound(section.name, "Folder")
        if time is None:
            raise ExceptionNotFound(section.name, "UpdateTime")
        if self._region_id is None:
            raise ExceptionNotFound(section.name, "RegionId")
        if self._lat is None:
            raise ExceptionNotFound(section.name, "Lat")
        if self._lon is None:
            raise ExceptionNotFound(section.name, "Lon")

        if self._icon_scale is None:
            raise ExceptionNotFound(section.name, "IconScale")
        if self._icon_pos is None:
            raise ExceptionNotFound(section.name, "IconPos")

        if self._weather_type_pos is None:
            raise ExceptionNotFound(section.name, "WeatherTypePos")
        if self._temperature_pos is None:
            raise ExceptionNotFound(section.name, "TemperaturePos")
        if self._humidity_pos is None:
            raise ExceptionNotFound(section.name, "HumidityPos")
        if self._pressure_pos is None:
            raise ExceptionNotFound(section.name, "PressurePos")
        if self._wind_pos is None:
            raise ExceptionNotFound(section.name, "WindPos")

        if wt_name is None:
            raise ExceptionNotFound(section.name, "WeatherTypeFontName")
        if t_name is None:
            raise ExceptionNotFound(section.name, "TemperatureFontName")
        if h_name is None:
            raise ExceptionNotFound(section.name, "HumidityFontName")
        if p_name is None:
            raise ExceptionNotFound(section.name, "PressureFontName")
        if w_name is None:
            raise ExceptionNotFound(section.name, "WindFontName")

        if wt_size is None:
            raise ExceptionNotFound(section.name, "WeatherTypeFontSize")
        if t_size is None:
            raise ExceptionNotFound(section.name, "TemperatureFontSize")
        if h_size is None:
            raise ExceptionNotFound(section.name, "HumidityFontSize")
        if p_size is None:
            raise ExceptionNotFound(section.name, "PressureFontSize")
        if w_size is None:
            raise ExceptionNotFound(section.name, "WindFontSize")

        if wt_bold is None:
            raise ExceptionNotFound(section.name, "WeatherTypeFontBold")
        if t_bold is None:
            raise ExceptionNotFound(section.name, "TemperatureFontBold")
        if h_bold is None:
            raise ExceptionNotFound(section.name, "HumidityFontBold")
        if p_bold is None:
            raise ExceptionNotFound(section.name, "PressureFontBold")
        if w_bold is None:
            raise ExceptionNotFound(section.name, "WindFontBold")

        if wt_italic is None:
            raise ExceptionNotFound(section.name, "WeatherTypeFontItalic")
        if t_italic is None:
            raise ExceptionNotFound(section.name, "TemperatureFontItalic")
        if h_italic is None:
            raise ExceptionNotFound(section.name, "HumidityFontItalic")
        if p_italic is None:
            raise ExceptionNotFound(section.name, "PressureFontItalic")
        if w_italic is None:
            raise ExceptionNotFound(section.name, "WindFontItalic")

        if len(self._icon_scale) != 2:
            raise ExceptionFormat(section.name, "IconScale")
        if len(self._icon_pos) != 2:
            raise ExceptionFormat(section.name, "IconPos")
        if len(self._weather_type_pos) != 2:
            raise ExceptionFormat(section.name, "WeatherTypePos")
        if len(self._temperature_pos) != 2:
            raise ExceptionFormat(section.name, "TemperaturePos")
        if len(self._humidity_pos) != 2:
            raise ExceptionFormat(section.name, "HumidityPos")
        if len(self._pressure_pos) != 2:
            raise ExceptionFormat(section.name, "PressurePos")
        if len(self._wind_pos) != 2:
            raise ExceptionFormat(section.name, "WindPos")

        self._weather_type_font = pygame.font.SysFont(wt_name, wt_size, wt_bold, wt_italic)
        self._temperature_font = pygame.font.SysFont(t_name, t_size, t_bold, t_italic)
        self._humidity_font = pygame.font.SysFont(h_name, h_size, h_bold, h_italic)
        self._pressure_font = pygame.font.SysFont(p_name, p_size, p_bold, p_italic)
        self._wind_font = pygame.font.SysFont(w_name, w_size, w_bold, w_italic)

        if not os.path.exists(self._folder):
            os.mkdir(self._folder)
        # for image_name in ["01d.png", "01n.png", "02d.png", "02n.png", "03d.png", "03n.png",
        #                   "04d.png", "04n.png", "09d.png", "09n.png", "10d.png", "10n.png",
        #                   "11d.png", "11n.png", "13d.png", "13n.png", "50d.png", "50n.png"]:
        #     self._load(image_name, self._folder)

        self.update_info(True)
        self.set_time(time)

    def update_info(self, is_online):
        try:
            if not is_online:
                return
            self.execute()
        except Exception as ex:
            self._logger.exception(ex)

    def update_display(self, is_online: bool, screen, size, fore_color, back_color, current_time) -> None:
        try:
            if not is_online:
                return

            if self._weather_image is not None:
                screen.blit(self._weather_image, self._icon_pos)
            if self._weather_type is not None:
                text = "{0}".format(self._weather_type)
                surf = self._weather_type_font.render(text, True, fore_color, back_color)
                screen.blit(surf, self._weather_type_pos)
            if self._temperature is not None:
                text = "{0:+.0f}°".format(self._temperature)
                surf = self._temperature_font.render(text, True, fore_color, back_color)
                screen.blit(surf, self._temperature_pos)
            if self._humidity is not None:
                text = "Влажность {0}%".format(self._humidity)
                surf = self._humidity_font.render(text, True, fore_color, back_color)
                screen.blit(surf, self._humidity_pos)
            if self._pressure is not None:
                text = "Давление {0} мм".format(self._pressure)
                surf = self._pressure_font.render(text, True, fore_color, back_color)
                screen.blit(surf, self._pressure_pos)
            if self._wind_speed is not None:
                text = "Ветер {0} м/с {1}".format(self._wind_speed, self._wind_direction)
                surf = self._wind_font.render(text, True, fore_color, back_color)
                screen.blit(surf, self._wind_pos)
        except Exception as ex:
            self._logger.exception(ex)

    def execute(self, *args) -> None:
        data = self._get_data()
        if data is None:
            return

        root = ET.fromstring(data)
        self._weather_type = str(root.find("weather/day/day_part/weather_type").text).capitalize()
        self._temperature = float(root.find("weather/day/day_part/temperature").text)
        self._humidity = str(root.find("weather/day/day_part/dampness").text)
        self._pressure = str(root.find("weather/day/day_part/pressure").text)
        self._wind_speed = str(root.find("weather/day/day_part/wind_speed").text)
        self._wind_direction = str(root.find("weather/day/day_part/wind_direction").text)

        load_path = root.find("weather/day/day_part/image-v3").text
        image_name = os.path.basename(load_path)
        self._load(image_name, self._folder, load_path)
        image_name = os.path.join(self._folder, image_name)
        self._weather_image = pygame.transform.smoothscale(pygame.image.load(image_name), self._icon_scale)

        self._text = WEATHER_TEXT_FORMAT.format(
            self._weather_type,
            self._temperature,
            self._wind_speed,
            self._humidity,
            self._pressure)

    def _load(self, image_name, path, url):
        file_path = os.path.join(path, image_name)
        if not os.path.exists(file_path):
            with open(file_path, "wb") as file:
                file.write(request.urlopen(url).read())

    def _get_data(self):
        dif = datetime.now() - self._last_update
        if dif.seconds >= MIN_UPDATE_TIME:
            url_path = "https://export.yandex.ru/bar/reginfo.xml?regionid={0}&lat={1}&lon={2}".format(
                self._region_id, self._lat, self._lon)
            with request.urlopen(url_path) as file:
                data = file.read()
            with open(os.path.join(self._folder, WEATHER_FILE), "wb") as file:
                file.write(data)
            self._last_update = datetime.now()
            return data
        with open(os.path.join(self._folder, WEATHER_FILE), "rb") as file:
            return file.read()
