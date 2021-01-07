import datetime
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
from modules.block_player import BlockPlayer
from modules.block_voice import BlockVoice
from modules.block_alarm import BlockAlarm
from modules.block_swap import BlockSwap
# from modules.block_wunderground import BlockWunderGround
from modules.block_watcher import BlockWatcher
from modules.block_mt8057 import BlockMT8057
from modules.block_yandex_weather import BlockYandexWeather
from modules.block_bme280 import BlockBme280
from modules.block_volume import BlockVolume
from modules.block_ir import BlockIR

from modules.hal.halgpio import HalGpio
from modules.hal.bme280_base import Bme280_Base
from modules.hal.lirc_base import Lirc_Base

logging.config.fileConfig("logger.ini")
logger = logging.getLogger("root")

FPS = 60
# WAIT_TIME = 40
IDLE_EVENT = (pygame.locals.USEREVENT + 1)


class Mainboard:

    def __init__(self, hal: HalGpio, hal_bme280: Bme280_Base, hal_lirc: Lirc_Base, setting_file: str):
        """ """
        self._modules = []
        self._size = None
        self._screen = None
        self._is_display_on = True
        self._logger = logger
        # Загружаем настройки из конфиг файла
        self._config = Setting()
        self._config.load(setting_file)
        self._hal = hal(logger, self.display_on, self._config.PIR_Pin, self._config.LED_Pin)
        self._manager_list = {
            "Time": BlockTime(logger, self._config),
            "Alarm": BlockAlarm(logger, self._config),
            "Player": BlockPlayer(logger, self._config),
            "Voice": BlockVoice(logger, self._config),
            "YandexNews": BlockYandexNews(logger, self._config),
            "OpenWeatherMap": BlockOpenWeatherMap(logger, self._config),
            # "WunderGround": BlockWunderGround(logger, self._config),
            "Calendar": BlockCalendar(logger, self._config),
            "Swap": BlockSwap(logger, self._config),
            "Watcher": BlockWatcher(logger, self._config),
            "MT8057": BlockMT8057(logger, self._config),
            "YandexWeather": BlockYandexWeather(logger, self._config),
            "BME280": BlockBme280(logger, self._config, hal_bme280),
            "Volume": BlockVolume(logger, self._config),
            "IR": BlockIR(logger, self._config, hal_lirc),
        }

        for name in self._config._block_list:
            if name in self._manager_list:
                self._modules.append(self._manager_list[name])
                print(name)

        # Инициализируем PyGame
        pygame.init()
        # Инициализируем шрифты
        pygame.font.init()
        # Инициализируем музыкальный модуль https://wiki.libsdl.org/FAQUsingSDL
        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.0)

        # Инициализируем драйвер дисплея https://wiki.libsdl.org/FAQUsingSDL
        pygame.display.init()

        flags = pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE if self._config.FullScreen else pygame.DOUBLEBUF | pygame.HWSURFACE
        self._size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        self._screen = pygame.display.set_mode(self._size, flags)

        print("Framebuffer size: {0}".format(self._size))

        # Выключаем курсор
        pygame.mouse.set_visible(False)

        for module in self._modules:
            try:
                module.init(self._manager_list)
            except Exception as ex:
                self._logger.exception(ex)

        pygame.time.set_timer(BLOCK_SECOND_UPDATE_EVENT, 1000)
        pygame.time.set_timer(BLOCK_MINUTE_UPDATE_EVENT, 60000)

    def __del__(self):
        """Destructor to make sure pygame shuts down, etc."""
        # pygame.display.quit()
        # pygame.mixer.quit()

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
        self._hal.init()
        try:
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

        except KeyboardInterrupt:
            pass

        for module in self._modules:
            module.done()

        pygame.quit()
        self._hal.done()
