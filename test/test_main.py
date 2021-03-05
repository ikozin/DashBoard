# import pytest
from exceptions import ExceptionNotFound
from setting import Setting
from modules.BlockBase import BlockBase
from logging import Logger
from modules.hal.halgpio import HalGpio
from typing import Callable
from time import time
import pygame


# @pytest.mark.block_main
# def test_main(logger, mocker):
#     log("run")
#     app = StubMainboard(StubHalGpio, logger)
#     app.loop()

class StubMainboard:

    def __init__(self, hal: HalGpio, logger: Logger):
        """ """
        self._is_display_on = True
        self._logger = logger
        self._hal = hal(logger, self.display_on)
        self._idle_event = pygame.event.custom_type()
        self.display_on()

    def __del__(self):
        pass

    def set_display_timer_on(self) -> None:
        log("set_display_timer_on")
        pygame.time.set_timer(self._idle_event, 0)
        pygame.time.set_timer(self._idle_event, 2000)

    def set_display_timer_off(self) -> None:
        log("set_display_timer_off")
        pygame.time.set_timer(self._idle_event, 0)

    def display_off(self) -> None:
        log("display_off")
        if not self._is_display_on:
            return
        self._is_display_on = False
        self._hal.display_off()
        self._hal.ledOff()
        self.set_display_timer_off()

    def display_on(self) -> None:
        log("display_on")
        self.set_display_timer_on()
        if self._is_display_on:
            return
        self._is_display_on = True
        self._hal.display_on()
        self._hal.ledOn()

    def procced_event(self, events) -> int:
        for event in events:
            log(event)
            if event.type == pygame.locals.QUIT:
                return 0
            if event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_ESCAPE:
                return 0
            if event.type == self._idle_event:
                self.display_off()
                return 0
        return 1

    def loop(self) -> None:
        log("loop")
        self._hal.init()
        while self.procced_event(pygame.event.get(eventtype=None, pump=True)):
            self._hal.update()

        #pygame.quit()
        self._hal.done()


class StubHalGpio(HalGpio):

    def __init__(self, logger: Logger, func: Callable[[], None]):
        super(StubHalGpio, self).__init__(logger, func, 0, 0)
        self._cnt = 0
        self._time = time()

    def init(self) -> None:
        pass

    def done(self) -> None:
        pass

    def update(self) -> None:
        if time() - self._time > 1:
            self._time = time()
            log("update")
            if self._cnt < 5:
                self._cnt = self._cnt + 1
                self._func()
        pass

    def display_off(self) -> None:
        pass

    def display_on(self) -> None:
        pass

    def reboot(self) -> None:
        pass

    def shutdown(self) -> None:
        pass

    def ledOn(self) -> None:
        pass

    def ledOff(self) -> None:
        pass


def log(message) -> None:
    print(pygame.time.get_ticks(), message)
