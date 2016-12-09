import os
import sys
import urllib.request as request
import xml.etree.ElementTree as ET
import configparser
import pygame
from datetime  import datetime, timedelta

from exceptions import ExceptionFormat, ExceptionNotFound
from modules.BlockMinuteBase import BlockMinuteBase

##############################################################
# http://openweathermap.org/appid#work - 1 time per 10 minutes
##############################################################
MIN_UPDATE_TIME = 600
CITY_ID = 524901
WEATHER_FILE = "openweathermap_data.xml"
WEATHER_TEXT_FORMAT = "{0}, Температура {1:+.1f}°, Скорость ветра {2} метра в секунду, Влажность {3}%, Давление {4} мм ртутного столба"
DETAILS_TEXT_FORMAT = "Ветер {0} м/с {1}\nВлажность {2}%\nДавление {3} мм"


class BlockOpenWeatherMap(BlockMinuteBase):
    """description of class"""

    def __init__(self, logger, setting):
        """Initializes (declare internal variables)"""
        super(BlockOpenWeatherMap, self).__init__(logger, setting)
        self._lastUpdate = datetime.now() - timedelta(seconds=MIN_UPDATE_TIME + 1)

        self._key = None
        self._folder = None

        self._weather_type = None
        self._temperature = None
        self._humidity = None
        self._pressure = None
        self._wind_speed = None
        self._wind_direction = None
        self._weather_image = None

        self._iconScale = None
        self._iconPos = None
        self._weatherTypePos = None
        self._temperaturePos = None
        self._humidityPos = None
        self._pressurePos = None
        self._windPos = None

        self._weatherTypeFont = None
        self._temperatureFont = None
        self._humidityFont = None
        self._pressureFont = None
        self._windFont = None


    def init(self, fileName, isOnline, modList):
        """Initializes (initialize internal variables)"""
        config = configparser.ConfigParser()
        config.read(fileName, "utf-8")
        section = config["OpenWeatherMapBlock"]

        self._key = section.get("Key")
        self._folder = section.get("Folder")
        time = section.getint("UpdateTime")

        self._iconScale = self._getTuple(section.get("IconScale"))
        self._iconPos = self._getTuple(section.get("IconPos"))
        self._weatherTypePos = self._getTuple(section.get("WeatherTypePos"))
        self._temperaturePos = self._getTuple(section.get("TemperaturePos"))
        self._humidityPos = self._getTuple(section.get("HumidityPos"))
        self._pressurePos = self._getTuple(section.get("PressurePos"))
        self._windPos = self._getTuple(section.get("WindPos"))

        wtName = section.get("WeatherTypeFontName")
        tName  = section.get("TemperatureFontName")
        hName  = section.get("HumidityFontName")
        pName  = section.get("PressureFontName")
        wName  = section.get("WindFontName")

        wtSize = section.getint("WeatherTypeFontSize")
        tSize  = section.getint("TemperatureFontSize")
        hSize  = section.getint("HumidityFontSize")
        pSize  = section.getint("PressureFontSize")
        wSize  = section.getint("WindFontSize")

        wtBold = section.getboolean("WeatherTypeFontBold")
        tBold  = section.getboolean("TemperatureFontBold")
        hBold  = section.getboolean("HumidityFontBold")
        pBold  = section.getboolean("PressureFontBold")
        wBold  = section.getboolean("WindFontBold")

        wtItalic = section.getboolean("WeatherTypeFontItalic")
        tItalic  = section.getboolean("TemperatureFontItalic")
        hItalic  = section.getboolean("HumidityFontItalic")
        pItalic  = section.getboolean("PressureFontItalic")
        wItalic  = section.getboolean("WindFontItalic")

        if self._key is None:    raise ExceptionNotFound(section.name, "Key")
        if self._folder is None: raise ExceptionNotFound(section.name, "Folder")
        if time is None:         raise ExceptionNotFound(section.name, "UpdateTime")

        if self._iconScale is None: raise ExceptionNotFound(section.name, "IconScale")
        if self._iconPos is None:   raise ExceptionNotFound(section.name, "IconPos")

        if self._weatherTypePos is None: raise ExceptionNotFound(section.name, "WeatherTypePos")
        if self._temperaturePos is None: raise ExceptionNotFound(section.name, "TemperaturePos")
        if self._humidityPos is None:    raise ExceptionNotFound(section.name, "HumidityPos")
        if self._pressurePos is None:    raise ExceptionNotFound(section.name, "PressurePos")
        if self._windPos is None:        raise ExceptionNotFound(section.name, "WindPos")

        if wtName is None: raise ExceptionNotFound(section.name, "WeatherTypeFontName")
        if tName is None:  raise ExceptionNotFound(section.name, "TemperatureFontName")
        if hName is None:  raise ExceptionNotFound(section.name, "HumidityFontName")
        if pName is None:  raise ExceptionNotFound(section.name, "PressureFontName")
        if wName is None:  raise ExceptionNotFound(section.name, "WindFontName")

        if wtSize is None: raise ExceptionNotFound(section.name, "WeatherTypeFontSize")
        if tSize is None:  raise ExceptionNotFound(section.name, "TemperatureFontSize")
        if hSize is None:  raise ExceptionNotFound(section.name, "HumidityFontSize")
        if pSize is None:  raise ExceptionNotFound(section.name, "PressureFontSize")
        if wSize is None:  raise ExceptionNotFound(section.name, "WindFontSize")

        if wtBold is None: raise ExceptionNotFound(section.name, "WeatherTypeFontBold")
        if tBold is None:  raise ExceptionNotFound(section.name, "TemperatureFontBold")
        if hBold is None:  raise ExceptionNotFound(section.name, "HumidityFontBold")
        if pBold is None:  raise ExceptionNotFound(section.name, "PressureFontBold")
        if wBold is None:  raise ExceptionNotFound(section.name, "WindFontBold")

        if wtItalic is None: raise ExceptionNotFound(section.name, "WeatherTypeFontItalic")
        if tItalic  is None: raise ExceptionNotFound(section.name, "TemperatureFontItalic")
        if hItalic  is None: raise ExceptionNotFound(section.name, "HumidityFontItalic")
        if pItalic  is None: raise ExceptionNotFound(section.name, "PressureFontItalic")
        if wItalic  is None: raise ExceptionNotFound(section.name, "WindFontItalic")


        if len(self._iconScale) != 2:      raise ExceptionFormat(section.name, "IconScale")
        if len(self._iconPos) != 2:        raise ExceptionFormat(section.name, "IconPos")
        if len(self._weatherTypePos) != 2: raise ExceptionFormat(section.name, "WeatherTypePos")
        if len(self._temperaturePos) != 2: raise ExceptionFormat(section.name, "TemperaturePos")
        if len(self._humidityPos) != 2:    raise ExceptionFormat(section.name, "HumidityPos")
        if len(self._pressurePos) != 2:    raise ExceptionFormat(section.name, "PressurePos")
        if len(self._windPos) != 2:        raise ExceptionFormat(section.name, "WindPos")

        self._weatherTypeFont = pygame.font.SysFont(wtName, wtSize, wtBold, wtItalic)
        self._temperatureFont = pygame.font.SysFont(tName, tSize, tBold, tItalic)
        self._humidityFont = pygame.font.SysFont(hName, hSize, hBold, hItalic)
        self._pressureFont = pygame.font.SysFont(pName, pSize, pBold, pItalic)
        self._windFont = pygame.font.SysFont(wName, wSize, wBold, wItalic)

        if not os.path.exists(self._folder):
            os.mkdir(self._folder)
        for imageName in ["01d.png","01n.png","02d.png","02n.png","03d.png","03n.png",
                          "04d.png","04n.png","09d.png","09n.png","10d.png","10n.png",
                          "11d.png","11n.png","13d.png","13n.png","50d.png","50n.png"]:
            self._load(imageName, self._folder)

        self.updateInfo(isOnline)
        self.setTime(time)


    def updateInfo(self, isOnline):
        try:
            if not isOnline: return

            data = self._getData()
            if data is None: return

            root = ET.fromstring(data)
            self._weather_type = str(root.find("weather").attrib["value"]).capitalize()
            self._temperature = float(root.find("temperature").attrib["value"])
            self._humidity = str(root.find("humidity").attrib["value"])
            self._pressure = str(root.find("pressure").attrib["value"])
            self._wind_speed = str(root.find("wind/speed").attrib["value"])
            self._wind_direction = str(root.find("wind/direction").attrib["code"])

            imageName = str(root.find("weather").attrib["icon"]) + ".png"
            self._load(imageName, self._folder)
            imageName = os.path.join(self._folder, imageName)
            self._weather_image = pygame.transform.smoothscale(pygame.image.load(imageName), self._iconScale)

            self._text = WEATHER_TEXT_FORMAT.format(self._weather_type, self._temperature, self._wind_speed, self._humidity, self._pressure)
        except Exception as ex:
            self._logger.exception(ex)


    def updateDisplay(self, isOnline, screen, size, foreColor, backColor, current_time):
        try:
            if not isOnline: return

            if (self._weather_image is not None):
                screen.blit(self._weather_image, self._iconPos)
            if (self._weather_type is not None):
                text = "{0}".format(self._weather_type)
                surf = self._weatherTypeFont.render(text, True, foreColor, backColor)
                screen.blit(surf, self._weatherTypePos)
            if (self._temperature is not None):
                text = "{0:+.1f}°".format(self._temperature)
                surf = self._temperatureFont.render(text, True, foreColor, backColor)
                screen.blit(surf, self._temperaturePos)
            if (self._humidity is not None):
                text = "Влажность {0}%".format(self._humidity)
                surf = self._humidityFont.render(text, True, foreColor, backColor)
                screen.blit(surf, self._humidityPos)
            if (self._pressure is not None):
                text = "Давление {0} мм".format(self._pressure)
                surf = self._pressureFont.render(text, True, foreColor, backColor)
                screen.blit(surf, self._pressurePos)
            if (self._wind_speed is not None):
                text = "Ветер {0} м/с {1}".format(self._wind_speed, self._wind_direction)
                surf = self._windFont.render(text, True, foreColor, backColor)
                screen.blit(surf, self._windPos)
        except Exception as ex:
            self._logger.exception(ex)


    def _load(self, imageName, path):
        filePath = os.path.join(path, imageName);
        if not os.path.exists(filePath):
            url = "http://openweathermap.org/img/w/{0}".format(imageName)
            with open(filePath, "wb") as file:
                file.write(request.urlopen(url).read())


    def _getData(self):
        dif = datetime.now() - self._lastUpdate
        ##############################################################
        # http://openweathermap.org/appid#work - 1 time per 10 minutes
        ##############################################################
        if dif.seconds >= MIN_UPDATE_TIME:
            with request.urlopen("http://api.openweathermap.org/data/2.5/weather?id={0}&mode=xml&units=metric&lang=ru&APPID={1}".format(CITY_ID, self._key)) as f:
                data = f.read()
            with open(os.path.join(self._folder, WEATHER_FILE), "wb") as file:
                file.write(data)
            self._lastUpdate = datetime.now()
            return data
        else:
            with open(os.path.join(self._folder, WEATHER_FILE), "rb") as file:
                return file.read()
