import datetime
import os
import sys
import subprocess
import configparser
import locale
import pygame
import pygame.locals

FPS = 30
# WAIT_TIME = 40
BLOCK_TIME_DISPLAY_FORMAT = "{:%H:%M}"


class Mainboard:

    def __init__(self):
        """ """
        self._modules = []
        self._size = None
        self._screen = None

        # Based on "Python GUI in Linux frame buffer"
        # http://www.karoltomala.com/blog/?p=679
        # Check which frame buffer drivers are available
        # Start with fbcon since directfb hangs with composite output
        drivers = ["fbcon", "directfb", "svgalib", "xvfb", "x11", "windib", "directx"]
        found = False
        for driver in drivers:
            # Make sure that SDL_VIDEODRIVER is set
            if not os.getenv("SDL_VIDEODRIVER"):
                os.putenv("SDL_VIDEODRIVER", driver)
            try:
                pygame.display.init()
            except pygame.error:
                print("Driver: {0} failed.".format(driver))
                continue
            found = True
            break

        if not found:
            raise Exception("No suitable video driver found!")
        self._size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        self._screen = pygame.display.set_mode(self._size, pygame.FULLSCREEN | pygame.HWSURFACE)
        print("Framebuffer size: {0}".format(self._size))

        # Инициализируем шрифты
        pygame.font.init()
        # Инициализируем музыкальный модуль
        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.0)

        # Выключаем курсор
        pygame.mouse.set_visible(False)

        self._font = pygame.font.SysFont("Helvetica", 256, True, False)


    def __del__(self):
        """Destructor to make sure pygame shuts down, etc."""
        pygame.mixer.quit()
        pygame.display.quit()


    def proccedEvent(self, events):
        for event in events:
            if (event.type == pygame.locals.QUIT):
                return 0
            if (event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_ESCAPE):
                return 0
        return 1

    def loop(self):
        clock = pygame.time.Clock()
        while (self.proccedEvent(pygame.event.get())):

            self._screen.fill((0, 0, 0))

            time = datetime.datetime.now()
            text = BLOCK_TIME_DISPLAY_FORMAT.format(time)
            sz = self._font.size(text)
            x = (self._size[0] - sz[0]) >> 1
            y = (self._size[1] - sz[1]) >> 1
            surf = self._font.render(text, True, (64, 64, 64), (0, 0, 0))
            self._screen.blit(surf, (x, y))


            pygame.display.update()
            # pygame.display.flip()
            # pygame.time.delay(WAIT_TIME)
            clock.tick(FPS)

        pygame.quit()


if __name__ == "__main__":

    print(pygame.version.ver)
    app = Mainboard()
    app.loop()
    sys.exit(0)
