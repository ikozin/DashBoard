import os
import sys
import subprocess
import configparser
import logging
import logging.config
import logging.handlers
import locale
import pygame
import pygame.locals

from setting import Setting
from modules.BlockTime import BlockTime
from modules.BlockCalendar import BlockCalendar
from modules.BlockYandexNews import BlockYandexNews
from modules.BlockOpenWeatherMap import BlockOpenWeatherMap
from modules.BlockVoice import BlockVoice
from modules.BlockTextAgregator import BlockTextAgregator
from modules.BlocklAlarm import BlocklAlarm
from modules.BlockSwap import BlockSwap
from modules.BlockWunderGround import BlockWunderGround

logging.config.fileConfig("logger.ini")
logger = logging.getLogger("root")

FILE_SETTING = "setting.ini"
PIR_PIN      = 13                #GPIO27 green
LED_PIN      = 12                #GPIO18 red
IDLE_EVENT   = (pygame.locals.USEREVENT + 1)

###########################################################################
if sys.platform == "linux": # Only for Raspberry Pi
    import RPi.GPIO as GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.setup(PIR_PIN, GPIO.IN)
    GPIO.output(LED_PIN, 1)


    def motionDetected(pin):
        #logger.debug("Motion detected!")
        app.displayOn()    
###########################################################################

class Mainboard :

    def __init__(self):
        """Initializes a new pygame screen using the framebuffer"""
        self._modules  = []
        self._size = None
        self._screen = None
        self._isDisplayOn = True
        # Загружаем настройки из конфиг файла
        self._config = Setting()
        self._config.load(FILE_SETTING) 
        # Based on "Python GUI in Linux frame buffer"
        # http://www.karoltomala.com/blog/?p=679
        # Check which frame buffer drivers are available
        # Start with fbcon since directfb hangs with composite output
        drivers = ["fbcon", "directfb", "svgalib", "xvfb", "x11", "directx", "windib"]
        found = False
        for driver in drivers:
            # Make sure that SDL_VIDEODRIVER is set
            if not os.getenv("SDL_VIDEODRIVER"):
                os.putenv("SDL_VIDEODRIVER", driver)
            try:
                pygame.display.init()
            except pygame.error:
                print ("Driver: {0} failed.".format(driver))
                continue
            found = True
            break
    
        if not found:
            raise Exception("No suitable video driver found!")
        
        if sys.platform == "linux": # Only for Raspberry Pi
            self._size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
            self._screen = pygame.display.set_mode(self._size, pygame.FULLSCREEN | pygame.HWSURFACE)
        else:
            self._size = (1280, 1024)
            self._screen = pygame.display.set_mode(self._size)

        print("Framebuffer size: {0}".format(self._size))

        # Инициализируем шрифты
        pygame.font.init()
        # Инициализируем музыкальный модуль
        pygame.mixer.init(16000, -16, 2, 512)
        pygame.mixer.music.set_volume(0.0)

        # Выключаем курсор
        pygame.mouse.set_visible(False)

        self._modules.append(BlockTime(logger, self._config))
        #self._modules.append(BlockOpenWeatherMap(logger, self._config))
        #self._modules.append(BlockCalendar(logger, self._config))
        blockSwap = BlockSwap(logger, self._config)
        #blockSwap.AddBlocks(BlockOpenWeatherMap(logger, self._config), BlockCalendar(logger, self._config))
        blockSwap.AddBlocks(BlockWunderGround(logger, self._config), BlockCalendar(logger, self._config))
        self._modules.append(blockSwap)
        self._modules.append(BlockYandexNews(logger, self._config))

        argergator = BlockTextAgregator(logger, self._config)
        argergator.addBlock(self._modules[0])
        argergator.addBlock(self._modules[1])
        argergator.addBlock(self._modules[2])
        voice = BlockVoice(logger, self._config)
        voice.setTextSource(argergator)
        self._modules.append(voice)
        self._modules.append(argergator)
        
        alarm = BlocklAlarm(logger, self._config)
        alarm.addBlock(self._modules[0])
        alarm.addBlock(self._modules[1])
        alarm.addBlock(self._modules[2])
        self._modules.append(alarm)

        for module in self._modules:
            module.init(FILE_SETTING)
            module.updateInfo(self._isDisplayOn)


    def __del__(self):
        """Destructor to make sure pygame shuts down, etc."""
        #pygame.mixer.quit()
        #pygame.display.quit()


    def setDisplayTimerOn(self):
        """Таймер для отключения дисплея"""
        (start, backgroundColor, foregroundColor, idleTime) = self._config.get_curret_setting()
        pygame.time.set_timer(IDLE_EVENT, 0)
        pygame.time.set_timer(IDLE_EVENT, idleTime * 60000)


    def setDisplayTimerOff(self):
        """Таймер для отключения дисплея"""
        pygame.time.set_timer(IDLE_EVENT, 0)


    def displayOff(self):
        if (self._isDisplayOn == False):
            return
        ###########################################################################
        if sys.platform == "linux": # Only for Raspberry Pi
            subprocess.Popen("/opt/vc/bin/tvservice -o > /dev/null 2>&1", shell=True)
            GPIO.output(LED_PIN, 0)
        else:
            pass
        ###########################################################################
        self.setDisplayTimerOff()
        self._isDisplayOn = False


    def displayOn(self):
        self.setDisplayTimerOn()
        if (self._isDisplayOn == True):
            return
        ###########################################################################
        if sys.platform == "linux": # Only for Raspberry Pi
            subprocess.Popen("/opt/vc/bin/tvservice -p > /dev/null 2>&1", shell=True)
            GPIO.output(LED_PIN, 1)
        else:
            pass
        ###########################################################################
        self._isDisplayOn = True
        for module in self._modules:
            module.updateInfo(self._isDisplayOn)


    def proccedEvent(self, events): 
        for event in events: 
            if (event.type == pygame.locals.QUIT) or (event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_ESCAPE):
                return 0
            if (event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_r):
                ###########################################################################
                if sys.platform == "linux": # Only for Raspberry Pi
                    subprocess.Popen("sudo reboot", shell=True)
                else:
                    pass
                ###########################################################################
                return 0
            if (event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_h):
                ###########################################################################
                if sys.platform == "linux": # Only for Raspberry Pi
                    subprocess.Popen("sudo shutdown -h now", shell=True)
                else:
                    pass
                ###########################################################################
                return 0
            if (event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_o):
                self.displayOff()
            if (event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_p):
                self.displayOn()
            if event.type == IDLE_EVENT:
                self.displayOff()

            for module in self._modules:
                module.proccedEvent(event, self._isDisplayOn)
        return 1


    def loop(self):
        while (self.proccedEvent(pygame.event.get())):

            (start, backgroundColor, foregroundColor, idleTime) = self._config.get_curret_setting()
            self._screen.fill(backgroundColor)

            for module in self._modules:
                module.updateDisplay(self._isDisplayOn, self._screen, self._size, foregroundColor, backgroundColor)

            pygame.display.update()
            pygame.time.delay(50)

        pygame.quit()


if __name__ == "__main__":

    print(pygame.version.ver)
    # Create an instance of the mainboard class
    app = Mainboard()

    ###########################################################################
    if sys.platform == "linux": # Only for Raspberry Pi
        GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=motionDetected)
    ###########################################################################

    app.loop()

    ###########################################################################
    if sys.platform == "linux": # Only for Raspberry Pi
        GPIO.cleanup()
    ###########################################################################

    sys.exit(0)
