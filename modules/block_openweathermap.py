import os
import sys
import urllib.request as request
import xml.etree.ElementTree as ET
import configparser 
import pygame
import pygame.locals
from datetime  import datetime, timedelta

from block_base import BlockBase
from setting import TEXT_EXCEPTION_NOT_FOUND
from setting import TEXT_EXCEPTION_FORMAT


##############################################################
# http://openweathermap.org/appid#work - 1 time per 10 minutes 
##############################################################
MIN_UPDATE_TIME = 600
CITY_ID = 524901
WEATHER_FILE = "data.xml"
WEATHER_TEXT_FORMAT = "{0}, Температура {1:+d}°, Скорость ветра {2} метра в секунду, Влажность {3:d}%, Давление {4:d} мм ртутного столба"
DETAILS_TEXT_FORMAT = "Ветер {0} м/с {1}\nВлажность {2}%\nДавление {3} мм"
BLOCK_OPEN_WEATHER_MAP_UPDATE_EVENT = (pygame.locals.USEREVENT + 4)

class BlockOpenWeatherMap(BlockBase):
    """description of class"""

    def __init__(self, logger):
        """Ininitializes"""
        super(BlockOpenWeatherMap, self).__init__(logger)
        self._lastUpdate = datetime.now() - timedelta(seconds=MIN_UPDATE_TIME + 1)

        self._key = None
        self._time = None
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

        self._weatherTypeFontName = None
        self._temperatureFontName = None
        self._humidityFontName = None
        self._pressureFontName = None
        self._windFontName = None

        self._weatherTypeFontSize = None
        self._temperatureFontSize = None
        self._humidityFontSize = None
        self._pressureFontSize = None
        self._windFontSize = None


    def init(self, fileName):
        config = configparser.ConfigParser()
        config.read(fileName, encoding="utf-8")
        section = config["OpenWeatherMapBlock"]

        self._key = section.get("Key")
        self._time = section.getint("UpdateTime")
        self._folder = section.get("Folder")

        self._iconScale = self._getTuple(section.get("IconScale"))
        self._iconPos = self._getTuple(section.get("IconPos"))
        self._weatherTypePos = self._getTuple(section.get("WeatherTypePos"))
        self._temperaturePos = self._getTuple(section.get("TemperaturePos"))
        self._humidityPos = self._getTuple(section.get("HumidityPos"))
        self._pressurePos = self._getTuple(section.get("PressurePos"))
        self._windPos = self._getTuple(section.get("WindPos"))


        self._weatherTypeFontName = section.get("WeatherTypeFontName")
        self._temperatureFontName = section.get("TemperatureFontName")
        self._humidityFontName = section.get("HumidityFontName")
        self._pressureFontName = section.get("PressureFontName")
        self._windFontName = section.get("WindFontName")

        self._weatherTypeFontSize = section.getint("WeatherTypeFontSize")
        self._temperatureFontSize = section.getint("TemperatureFontSize")
        self._humidityFontSize = section.getint("HumidityFontSize")
        self._pressureFontSize = section.getint("PressureFontSize")
        self._windFontSize = section.getint("WindFontSize")

        if not self._key:    raise Exception(TEXT_EXCEPTION_NOT_FOUND.format("OpenWeatherMapBlock", "Key"))
        if not self._time:   raise Exception(TEXT_EXCEPTION_NOT_FOUND.format("OpenWeatherMapBlock", "UpdateTime"))
        if not self._folder: raise Exception(TEXT_EXCEPTION_NOT_FOUND.format("OpenWeatherMapBlock", "Folder"))

        if not self._iconScale:            raise Exception(TEXT_EXCEPTION_NOT_FOUND.format("OpenWeatherMapBlock", "IconScale"))
        if not self._iconPos:              raise Exception(TEXT_EXCEPTION_NOT_FOUND.format("OpenWeatherMapBlock", "IconPos"))
        if not self._weatherTypePos:       raise Exception(TEXT_EXCEPTION_NOT_FOUND.format("OpenWeatherMapBlock", "WeatherTypePos"))
        if not self._temperaturePos:       raise Exception(TEXT_EXCEPTION_NOT_FOUND.format("OpenWeatherMapBlock", "TemperaturePos"))
        if not self._humidityPos:          raise Exception(TEXT_EXCEPTION_NOT_FOUND.format("OpenWeatherMapBlock", "HumidityPos"))
        if not self._pressurePos:          raise Exception(TEXT_EXCEPTION_NOT_FOUND.format("OpenWeatherMapBlock", "PressurePos"))
        if not self._windPos:              raise Exception(TEXT_EXCEPTION_NOT_FOUND.format("OpenWeatherMapBlock", "WindPos"))

        if not self._weatherTypeFontName:  raise Exception(TEXT_EXCEPTION_NOT_FOUND.format("OpenWeatherMapBlock", "WeatherTypeFontName"))
        if not self._temperatureFontName:  raise Exception(TEXT_EXCEPTION_NOT_FOUND.format("OpenWeatherMapBlock", "TemperatureFontName"))
        if not self._humidityFontName:     raise Exception(TEXT_EXCEPTION_NOT_FOUND.format("OpenWeatherMapBlock", "HumidityFontName"))
        if not self._pressureFontName:     raise Exception(TEXT_EXCEPTION_NOT_FOUND.format("OpenWeatherMapBlock", "PressureFontName"))
        if not self._windFontName:         raise Exception(TEXT_EXCEPTION_NOT_FOUND.format("OpenWeatherMapBlock", "WindFontName"))

        if not self._weatherTypeFontSize:  raise Exception(TEXT_EXCEPTION_NOT_FOUND.format("OpenWeatherMapBlock", "WeatherTypeFontSize"))
        if not self._temperatureFontSize:  raise Exception(TEXT_EXCEPTION_NOT_FOUND.format("OpenWeatherMapBlock", "TemperatureFontSize"))
        if not self._humidityFontSize:     raise Exception(TEXT_EXCEPTION_NOT_FOUND.format("OpenWeatherMapBlock", "HumidityFontSize"))
        if not self._pressureFontSize:     raise Exception(TEXT_EXCEPTION_NOT_FOUND.format("OpenWeatherMapBlock", "PressureFontSize"))
        if not self._windFontSize:         raise Exception(TEXT_EXCEPTION_NOT_FOUND.format("OpenWeatherMapBlock", "WindFontSize"))

        if len(self._iconScale) != 2:      raise Exception(TEXT_EXCEPTION_FORMAT.format("OpenWeatherMapBlock", "IconScale"))
        if len(self._iconPos) != 2:        raise Exception(TEXT_EXCEPTION_FORMAT.format("OpenWeatherMapBlock", "IconPos"))
        if len(self._weatherTypePos) != 2: raise Exception(TEXT_EXCEPTION_FORMAT.format("OpenWeatherMapBlock", "WeatherTypePos"))
        if len(self._temperaturePos) != 2: raise Exception(TEXT_EXCEPTION_FORMAT.format("OpenWeatherMapBlock", "TemperaturePos"))
        if len(self._humidityPos) != 2:    raise Exception(TEXT_EXCEPTION_FORMAT.format("OpenWeatherMapBlock", "HumidityPos"))
        if len(self._pressurePos) != 2:    raise Exception(TEXT_EXCEPTION_FORMAT.format("OpenWeatherMapBlock", "PressurePos"))
        if len(self._windPos) != 2:        raise Exception(TEXT_EXCEPTION_FORMAT.format("OpenWeatherMapBlock", "WindPos"))


        if not os.path.exists(self._folder):
            os.mkdir(self._folder)
        for imageName in ["01d.png","01n.png",
                          "02d.png","02n.png",
                          "03d.png","03n.png",
                          "04d.png","04n.png",
                          "09d.png","09n.png",
                          "10d.png","10n.png",
                          "11d.png","11n.png",
                          "13d.png","13n.png",
                          "50d.png","50n.png"]:
            self._load(imageName, self._folder)

        pygame.time.set_timer(BLOCK_OPEN_WEATHER_MAP_UPDATE_EVENT, self._time * 60000)


    def proccedEvent(self, event, isOnline):
        if event.type == BLOCK_OPEN_WEATHER_MAP_UPDATE_EVENT:
            self.updateInfo(isOnline)


    def updateInfo(self, isOnline):
        try:
            if not isOnline: return

            data = self._getData()
            if not data: return

            root = ET.fromstring(data)
            self._weather_type = str(root.find("weather").attrib["value"]).capitalize()
            self._temperature = int(float(root.find("temperature").attrib["value"]))
            self._humidity = int(root.find("humidity").attrib["value"])
            self._pressure = int(root.find("pressure").attrib["value"])
            self._wind_speed = float(root.find("wind/speed").attrib["value"])
            self._wind_direction = str(root.find("wind/direction").attrib["code"])
    
            imageName = str(root.find("weather").attrib["icon"]) + ".png"
            self._load(imageName, self._folder)
            imageName = os.path.join(self._folder, imageName)
            self._weather_image = pygame.transform.smoothscale(pygame.image.load(imageName), self._iconScale)
    
            self._text = WEATHER_TEXT_FORMAT.format(self._weather_type, 
                                                    self._temperature, 
                                                    self._wind_speed, 
                                                    self._humidity, 
                                                    self._pressure)
            #print (self._text)
        except Exception as ex:
            self._logger.exception(ex)
            self._text = None


    def updateDisplay(self, isOnline, screen, size, foreColor, backColor):
        try:
            if not isOnline: return
            if not self._text: return

            if (self._weather_image):
                screen.blit(self._weather_image, self._iconPos)
            if (self._weather_type):
                text = "{0}".format(self._weather_type)
                font = pygame.font.SysFont(self._weatherTypeFontName, self._weatherTypeFontSize)
                surf = font.render(text, True, foreColor, backColor)
                screen.blit(surf, self._weatherTypePos)
            if (self._temperature):
                text = "{0:+d}°".format(self._temperature)
                font = pygame.font.SysFont(self._temperatureFontName, self._temperatureFontSize)
                surf = font.render(text, True, foreColor, backColor)
                screen.blit(surf, self._temperaturePos)
            if (self._humidity):
                text = "Влажность {0}%".format(self._humidity)
                font = pygame.font.SysFont(self._humidityFontName, self._humidityFontSize)
                surf = font.render(text, True, foreColor, backColor)
                screen.blit(surf, self._humidityPos)
            if (self._pressure):
                text = "Давление {0} мм".format(self._pressure)
                font = pygame.font.SysFont(self._pressureFontName, self._pressureFontSize)
                surf = font.render(text, True, foreColor, backColor)
                screen.blit(surf, self._pressurePos)
            if (self._wind_speed):
                text = "Ветер {0} м/с {1}".format(self._wind_speed, self._wind_direction)
                font = pygame.font.SysFont(self._windFontName, self._windFontSize)
                surf = font.render(text, True, foreColor, backColor)
                screen.blit(surf, self._windPos)
        except Exception as ex:
            self._logger.exception(ex)


    def _load(self, imageName, path):
        filePath = os.path.join(path, imageName);
        if os.path.exists(filePath) == False:
            url = "http://openweathermap.org/img/w/{0}".format(imageName)
            file = open(filePath, "wb")
            file.write(request.urlopen(url).read())
            file.close()


    if sys.platform == "linux": # Only for Raspberry Pi
        def _getData(self):
            dif = datetime.now() - self._lastUpdate
            ##############################################################
            # http://openweathermap.org/appid#work - 1 time per 10 minutes 
            ##############################################################
            if dif.seconds >= MIN_UPDATE_TIME:
                data = request.urlopen("http://api.openweathermap.org/data/2.5/weather?id={0}&mode=xml&units=metric&lang=ru&APPID={1}".format(CITY_ID, self._key)).read()
                file = open(os.path.join(self._folder, WEATHER_FILE), "wb")
                file.write(data)
                file.close()
                self._lastUpdate = datetime.now()
            else:
                file = open(os.path.join(self._folder, WEATHER_FILE), "rb")
                data = file.read()
                file.close()
            return data
    else:
        def _getData(self):
            file = open(os.path.join(self._folder, WEATHER_FILE), "rb")
            data = file.read()
            file.close()
            return data


    def _getTuple(self, value):
        """ Конвертирует строку '0, 0, 0' в кортеж (0, 0, 0) """
        try:
            return tuple(int(item.strip("([ '])")) for item in value.split(",") if item.strip())
        except Exception as ex:
            self._logger.exception(ex)
            return None
