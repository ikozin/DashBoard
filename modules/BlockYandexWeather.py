import os
import urllib.request as request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from exceptions import ExceptionFormat, ExceptionNotFound
import pygame
from modules.BlockMinuteBase import BlockMinuteBase

MIN_UPDATE_TIME = 600
WEATHER_FILE = "yandexweather_data.xml"
WEATHER_TEXT_FORMAT = "{0}, Температура {1:+.0f}°, Скорость ветра {2} метра в секунду, " \
    "Влажность {3}%, Давление {4} мм ртутного столба"
DETAILS_TEXT_FORMAT = "Ветер {0} м/с {1}\nВлажность {2}%\nДавление {3} мм"


class BlockYandexWeather(BlockMinuteBase):
    """description of class"""

    def __init__(self, logger, setting):
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

    def init(self, mod_list):
        """Initializes (initialize internal variables)"""
        # Загружаем настройки
        section = self._setting.Configuration["YandexWeatherBlock"]

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

        wtName = section.get("WeatherTypeFontName")
        tName = section.get("TemperatureFontName")
        hName = section.get("HumidityFontName")
        pName = section.get("PressureFontName")
        wName = section.get("WindFontName")

        wtSize = section.getint("WeatherTypeFontSize")
        tSize = section.getint("TemperatureFontSize")
        hSize = section.getint("HumidityFontSize")
        pSize = section.getint("PressureFontSize")
        wSize = section.getint("WindFontSize")

        wtBold = section.getboolean("WeatherTypeFontBold")
        tBold = section.getboolean("TemperatureFontBold")
        hBold = section.getboolean("HumidityFontBold")
        pBold = section.getboolean("PressureFontBold")
        wBold = section.getboolean("WindFontBold")

        wtItalic = section.getboolean("WeatherTypeFontItalic")
        tItalic = section.getboolean("TemperatureFontItalic")
        hItalic = section.getboolean("HumidityFontItalic")
        pItalic = section.getboolean("PressureFontItalic")
        wItalic = section.getboolean("WindFontItalic")

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

        if wtName is None:
            raise ExceptionNotFound(section.name, "WeatherTypeFontName")
        if tName is None:
            raise ExceptionNotFound(section.name, "TemperatureFontName")
        if hName is None:
            raise ExceptionNotFound(section.name, "HumidityFontName")
        if pName is None:
            raise ExceptionNotFound(section.name, "PressureFontName")
        if wName is None:
            raise ExceptionNotFound(section.name, "WindFontName")

        if wtSize is None:
            raise ExceptionNotFound(section.name, "WeatherTypeFontSize")
        if tSize is None:
            raise ExceptionNotFound(section.name, "TemperatureFontSize")
        if hSize is None:
            raise ExceptionNotFound(section.name, "HumidityFontSize")
        if pSize is None:
            raise ExceptionNotFound(section.name, "PressureFontSize")
        if wSize is None:
            raise ExceptionNotFound(section.name, "WindFontSize")

        if wtBold is None:
            raise ExceptionNotFound(section.name, "WeatherTypeFontBold")
        if tBold is None:
            raise ExceptionNotFound(section.name, "TemperatureFontBold")
        if hBold is None:
            raise ExceptionNotFound(section.name, "HumidityFontBold")
        if pBold is None:
            raise ExceptionNotFound(section.name, "PressureFontBold")
        if wBold is None:
            raise ExceptionNotFound(section.name, "WindFontBold")

        if wtItalic is None:
            raise ExceptionNotFound(section.name, "WeatherTypeFontItalic")
        if tItalic is None:
            raise ExceptionNotFound(section.name, "TemperatureFontItalic")
        if hItalic is None:
            raise ExceptionNotFound(section.name, "HumidityFontItalic")
        if pItalic is None:
            raise ExceptionNotFound(section.name, "PressureFontItalic")
        if wItalic is None:
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

        self._weather_type_font = pygame.font.SysFont(wtName, wtSize, wtBold, wtItalic)
        self._temperature_font = pygame.font.SysFont(tName, tSize, tBold, tItalic)
        self._humidity_font = pygame.font.SysFont(hName, hSize, hBold, hItalic)
        self._pressure_font = pygame.font.SysFont(pName, pSize, pBold, pItalic)
        self._wind_font = pygame.font.SysFont(wName, wSize, wBold, wItalic)

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

    def update_display(self, is_online, screen, size, fore_color, back_color, current_time):
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

    def execute(self, *args):
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

        loadPath = root.find("weather/day/day_part/image-v3").text
        image_name = os.path.basename(loadPath)
        self._load(image_name, self._folder, loadPath)
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
            urlPath = "https://export.yandex.ru/bar/reginfo.xml?regionid={0}&lat={1}&lon={2}".format(
                self._region_id, self._lat, self._lon)
            with request.urlopen(urlPath) as f:
                data = f.read()
            with open(os.path.join(self._folder, WEATHER_FILE), "wb") as file:
                file.write(data)
            self._last_update = datetime.now()
            return data
        with open(os.path.join(self._folder, WEATHER_FILE), "rb") as file:
            return file.read()
