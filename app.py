import datetime
import os
import sys
import subprocess
import logging
import logging.config
import logging.handlers
import pygame

from setting import Setting
from setting import BLOCK_SECOND_UPDATE_EVENT
from setting import BLOCK_MINUTE_UPDATE_EVENT
from modules.BlockTime import BlockTime
from modules.BlockCalendar import BlockCalendar
from modules.BlockYandexNews import BlockYandexNews
from modules.BlockOpenWeatherMap import BlockOpenWeatherMap
from modules.BlockVoice import BlockVoice
from modules.BlockAlarm import BlockAlarm
from modules.BlockSwap import BlockSwap
from modules.BlockWunderGround import BlockWunderGround
from modules.BlockWatcher import BlockWatcher
from modules.BlockMT8057 import BlockMT8057
from modules.BlockYandexWeather import BlockYandexWeather
from modules.BlockIR import BlockIR

logging.config.fileConfig("logger.ini")
logger = logging.getLogger("root")

FPS = 60
# WAIT_TIME = 40
FILE_SETTING = "setting.ini"
PIR_PIN = 22  # GPIO22
LED_PIN = 23  # GPIO23
IDLE_EVENT = (pygame.locals.USEREVENT + 1)


###########################################################################
if sys.platform == "linux":  # Only for Raspberry Pi
    import RPi.GPIO as GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.setup(PIR_PIN, GPIO.IN)
    GPIO.output(LED_PIN, 1)

    def motion_detected(pin):
        # logger.debug("Motion detected!")
        app.display_on()
###########################################################################


class Mainboard:

    def __init__(self):
        """ """
        self._modules = []
        self._size = None
        self._screen = None
        self._is_display_on = True
        # Загружаем настройки из конфиг файла
        self._config = Setting()
        self._config.load(FILE_SETTING)

        self._manager_list = {
            "Time": BlockTime(logger, self._config),
            "Alarm": BlockAlarm(logger, self._config),
            "Voice": BlockVoice(logger, self._config),
            "YandexNews": BlockYandexNews(logger, self._config),
            "OpenWeatherMap": BlockOpenWeatherMap(logger, self._config),
            "WunderGround": BlockWunderGround(logger, self._config),
            "Calendar": BlockCalendar(logger, self._config),
            "Swap": BlockSwap(logger, self._config),
            "Watcher": BlockWatcher(logger, self._config),
            "MT8057": BlockMT8057(logger, self._config),
            "YandexWeather": BlockYandexWeather(logger, self._config),
            "IR": BlockIR(logger, self._config),
        }

        for name in self._config._block_list:
            if name in self._manager_list:
                self._modules.append(self._manager_list[name])
                print(name)

        # Based on "Python GUI in Linux frame buffer"
        # http://www.karoltomala.com/blog/?p=679
        # Check which frame buffer drivers are available
        # Start with fbcon since directfb hangs with composite output
        drivers = ["x11", "windib"]
        found = False
        for driver in drivers:
            # Make sure that SDL_VIDEODRIVER is set
            if not os.getenv("SDL_VIDEODRIVER"):
                os.putenv("SDL_VIDEODRIVER", driver)
            try:
                pygame.display.init()
            except Exception:
                print("Driver: {0} failed.".format(driver))
                continue
            found = True
            break

        if not found:
            raise Exception("No suitable video driver found!")
        ###########################################################################
        if sys.platform == "linux":  # Only for Raspberry Pi
            self._size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
            self._screen = pygame.display.set_mode(self._size, pygame.FULLSCREEN | pygame.HWSURFACE)
        else:
            self._size = (1824, 984)
            self._screen = pygame.display.set_mode(self._size)
        ###########################################################################
        print("Framebuffer size: {0}".format(self._size))

        # Инициализируем шрифты
        pygame.font.init()
        # Инициализируем музыкальный модуль
        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.0)

        # Выключаем курсор
        pygame.mouse.set_visible(False)

        for module in self._modules:
            module.init(self._manager_list)

        pygame.time.set_timer(BLOCK_SECOND_UPDATE_EVENT, 1000)
        pygame.time.set_timer(BLOCK_MINUTE_UPDATE_EVENT, 60000)

    def __del__(self):
        """Destructor to make sure pygame shuts down, etc."""
        # pygame.mixer.quit()
        # pygame.display.quit()

    def set_display_timer_on(self):
        """Таймер для отключения дисплея"""
        (_, _, _, idleTime) = self._config.get_curret_setting()
        pygame.time.set_timer(IDLE_EVENT, 0)
        pygame.time.set_timer(IDLE_EVENT, idleTime * 60000)

    def set_display_timer_off(self):
        """Таймер для отключения дисплея"""
        pygame.time.set_timer(IDLE_EVENT, 0)

    def display_off(self):
        if not self._is_display_on:
            return
        self._is_display_on = False
        ###########################################################################
        if sys.platform == "linux":  # Only for Raspberry Pi
            # https://news.screenly.io/how-to-automatically-turn-off-and-on-your-monitor-from-your-raspberry-pi-5f259f40cae5,
            # https://elinux.org/RPI_vcgencmd_usage
            subprocess.Popen("vcgencmd display_power 0 > /dev/null 2>&1", shell=True).wait()
            GPIO.output(LED_PIN, 0)
        else:
            pass
        ###########################################################################
        self.set_display_timer_off()

    def display_on(self):
        self.set_display_timer_on()
        if self._is_display_on:
            return
        self._is_display_on = True
        ###########################################################################
        if sys.platform == "linux":  # Only for Raspberry Pi
            # https://news.screenly.io/how-to-automatically-turn-off-and-on-your-monitor-from-your-raspberry-pi-5f259f40cae5,
            # https://elinux.org/RPI_vcgencmd_usage
            subprocess.Popen("vcgencmd display_power 1 > /dev/null 2>&1", shell=True).wait()
            GPIO.output(LED_PIN, 1)
        else:
            pass
        ###########################################################################
        for module in self._modules:
            module.update_info(self._is_display_on)

    def procced_event(self, events):
        for event in events:
            if event.type == pygame.locals.QUIT:
                return 0
            if event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_ESCAPE:
                return 0
            if event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_r:
                ###########################################################################
                if sys.platform == "linux":  # Only for Raspberry Pi
                    subprocess.Popen("sudo reboot", shell=True)
                else:
                    pass
                ###########################################################################
                return 0
            if event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_h:
                ###########################################################################
                if sys.platform == "linux":  # Only for Raspberry Pi
                    subprocess.Popen("sudo shutdown -h now", shell=True)
                else:
                    pass
                ###########################################################################
                return 0
            if event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_o:
                self.display_off()
            if event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_p:
                self.display_on()
            if event.type == IDLE_EVENT:
                self.display_off()

            for module in self._modules:
                module.procced_event(event, self._is_display_on)
        return 1

    def loop(self):
        clock = pygame.time.Clock()
        while self.procced_event(pygame.event.get()):

            if self._is_display_on:
                (_, background_color, foreground_color, _) = self._config.get_curret_setting()
                self._screen.fill(background_color)
                time = datetime.datetime.now()
                for module in self._modules:
                    module.update_display(
                        self._is_display_on,
                        self._screen,
                        self._size,
                        foreground_color,
                        background_color,
                        time)
            else:
                self._screen.fill((0, 0, 0))

            pygame.display.update()
            # pygame.time.delay(WAIT_TIME)
            clock.tick(FPS)

        for module in self._modules:
            module.done()

        pygame.quit()


if __name__ == "__main__":

    print(pygame.version.ver)
    # Create an instance of the Mainboard class
    app = Mainboard()

    ###########################################################################
    if sys.platform == "linux":  # Only for Raspberry Pi
        GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=motion_detected)
    ###########################################################################

    app.loop()

    ###########################################################################
    if sys.platform == "linux":  # Only for Raspberry Pi
        GPIO.cleanup()
    ###########################################################################
