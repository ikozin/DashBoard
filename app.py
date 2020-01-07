import datetime
import os
import logging
import logging.config
import logging.handlers
import pygame

from setting import Setting
from setting import BLOCK_SECOND_UPDATE_EVENT
from setting import BLOCK_MINUTE_UPDATE_EVENT
from modules.block_time import BlockTime
from modules.block_calendar import BlockCalendar
from modules.block_yandex_news import BlockYandexNews
from modules.block_open_weathermap import BlockOpenWeatherMap
from modules.block_voice import BlockVoice
from modules.block_alarm import BlockAlarm
from modules.block_swap import BlockSwap
from modules.block_wunderground import BlockWunderGround
from modules.block_watcher import BlockWatcher
from modules.block_mt8057 import BlockMT8057
from modules.block_yandex_weather import BlockYandexWeather
# from modules.block_ir import BlockIR

from halgpio import HalGpio

logging.config.fileConfig("logger.ini")
logger = logging.getLogger("root")

FPS = 60
# WAIT_TIME = 40
IDLE_EVENT = (pygame.locals.USEREVENT + 1)


class Mainboard:

    def __init__(self, hal: HalGpio, setting_file: str):
        """ """
        self._modules = []
        self._size = None
        self._screen = None
        self._is_display_on = True
        # Загружаем настройки из конфиг файла
        self._config = Setting()
        self._config.load(setting_file)
        self._hal = hal(logger, self.display_on)
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
            # "IR": BlockIR(logger, self._config),
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

        flags = pygame.FULLSCREEN | pygame.HWSURFACE if self._config.FullScreen else 0
        self._size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        self._screen = pygame.display.set_mode(self._size, flags)

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
        pass

    def set_display_timer_on(self) -> None:
        """Таймер для отключения дисплея"""
        (_, _, _, idle_time) = self._config.get_curret_setting()
        pygame.time.set_timer(IDLE_EVENT, 0)
        pygame.time.set_timer(IDLE_EVENT, idle_time * 60000)

    def set_display_timer_off(self) -> None:
        """Таймер для отключения дисплея"""
        pygame.time.set_timer(IDLE_EVENT, 0)

    def display_off(self) -> None:
        if not self._is_display_on:
            return
        self._is_display_on = False
        self._hal.display_off()
        self._hal.ledOff()
        self.set_display_timer_off()

    def display_on(self) -> None:
        self.set_display_timer_on()
        if self._is_display_on:
            return
        self._is_display_on = True
        self._hal.display_on()
        self._hal.ledOn()
        for module in self._modules:
            module.update_info(self._is_display_on)

    def procced_event(self, events) -> int:
        for event in events:
            if event.type == pygame.locals.QUIT:
                return 0
            if event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_ESCAPE:
                return 0
            if event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_r:
                self._hal.reboot()
                return 0
            if event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_h:
                self._hal.shutdown()
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

    def loop(self) -> None:
        print(pygame.version.ver)
        self._hal.init()
        clock = pygame.time.Clock()
        while self.procced_event(pygame.event.get()):

            self._hal.update()

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
        self._hal.done()
