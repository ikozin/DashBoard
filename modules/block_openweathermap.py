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
        """Initializes (declare internal variables)"""
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

        self._weatherTypeFont = None
        self._temperatureFont = None
        self._humidityFont = None
        self._pressureFont = None
        self._windFont = None


    def init(self, fileName):
        """Initializes (initialize internal variables)"""
        config = configparser.ConfigParser()
        config.read(fileName, "utf-8")
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

        if self._key is None:    raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(section.name, "Key"))
        if self._time is None:   raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(section.name, "UpdateTime"))
        if self._folder is None: raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(section.name, "Folder"))

        if self._iconScale is None: raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(section.name, "IconScale"))
        if self._iconPos is None:   raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(section.name, "IconPos"))

        if self._weatherTypePos is None: raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(section.name, "WeatherTypePos"))
        if self._temperaturePos is None: raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(section.name, "TemperaturePos"))
        if self._humidityPos is None:    raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(section.name, "HumidityPos"))
        if self._pressurePos is None:    raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(section.name, "PressurePos"))
        if self._windPos is None:        raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(section.name, "WindPos"))

        if wtName is None: raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(section.name, "WeatherTypeFontName"))
        if tName is None:  raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(section.name, "TemperatureFontName"))
        if hName is None:  raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(section.name, "HumidityFontName"))
        if pName is None:  raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(section.name, "PressureFontName"))
        if wName is None:  raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(section.name, "WindFontName"))

        if wtSize is None: raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(section.name, "WeatherTypeFontSize"))
        if tSize is None:  raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(section.name, "TemperatureFontSize"))
        if hSize is None:  raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(section.name, "HumidityFontSize"))
        if pSize is None:  raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(section.name, "PressureFontSize"))
        if wSize is None:  raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(section.name, "WindFontSize"))

        if wtBold is None: raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(section.name, "WeatherTypeFontBold"))
        if tBold is None:  raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(section.name, "TemperatureFontBold"))
        if hBold is None:  raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(section.name, "HumidityFontBold"))
        if pBold is None:  raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(section.name, "PressureFontBold"))
        if wBold is None:  raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(section.name, "WindFontBold"))

        if wtItalic is None: raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(section.name, "WeatherTypeFontItalic"))
        if tItalic  is None: raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(section.name, "TemperatureFontItalic"))
        if hItalic  is None: raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(section.name, "HumidityFontItalic"))
        if pItalic  is None: raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(section.name, "PressureFontItalic"))
        if wItalic  is None: raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(section.name, "WindFontItalic"))


        if len(self._iconScale) != 2:      raise Exception(TEXT_EXCEPTION_FORMAT.format(section.name, "IconScale"))
        if len(self._iconPos) != 2:        raise Exception(TEXT_EXCEPTION_FORMAT.format(section.name, "IconPos"))
        if len(self._weatherTypePos) != 2: raise Exception(TEXT_EXCEPTION_FORMAT.format(section.name, "WeatherTypePos"))
        if len(self._temperaturePos) != 2: raise Exception(TEXT_EXCEPTION_FORMAT.format(section.name, "TemperaturePos"))
        if len(self._humidityPos) != 2:    raise Exception(TEXT_EXCEPTION_FORMAT.format(section.name, "HumidityPos"))
        if len(self._pressurePos) != 2:    raise Exception(TEXT_EXCEPTION_FORMAT.format(section.name, "PressurePos"))
        if len(self._windPos) != 2:        raise Exception(TEXT_EXCEPTION_FORMAT.format(section.name, "WindPos"))

        self._weatherTypeFont = pygame.font.SysFont(wtName, wtSize, wtBold, wtItalic)
        self._temperatureFont = pygame.font.SysFont(tName, tSize, tBold, tItalic)
        self._humidityFont = pygame.font.SysFont(hName, hSize, hBold, hItalic)
        self._pressureFont = pygame.font.SysFont(pName, pSize, pBold, pItalic)
        self._windFont = pygame.font.SysFont(wName, wSize, wBold, wItalic)

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
            if data is None: return

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
            if self._text is None: return

            if (self._weather_image):
                screen.blit(self._weather_image, self._iconPos)
            if (self._weather_type):
                text = "{0}".format(self._weather_type)
                surf = self._weatherTypeFont.render(text, True, foreColor, backColor)
                screen.blit(surf, self._weatherTypePos)
            if (self._temperature):
                text = "{0:+d}°".format(self._temperature)
                surf = self._temperatureFont.render(text, True, foreColor, backColor)
                screen.blit(surf, self._temperaturePos)
            if (self._humidity):
                text = "Влажность {0}%".format(self._humidity)
                surf = self._humidityFont.render(text, True, foreColor, backColor)
                screen.blit(surf, self._humidityPos)
            if (self._pressure):
                text = "Давление {0} мм".format(self._pressure)
                surf = self._pressureFont.render(text, True, foreColor, backColor)
                screen.blit(surf, self._pressurePos)
            if (self._wind_speed):
                text = "Ветер {0} м/с {1}".format(self._wind_speed, self._wind_direction)
                surf = self._windFont.render(text, True, foreColor, backColor)
                screen.blit(surf, self._windPos)
        except Exception as ex:
            self._logger.exception(ex)


    def _load(self, imageName, path):
        filePath = os.path.join(path, imageName);
        if not os.path.exists(filePath):
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
