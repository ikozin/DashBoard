import sys
###########################################################################
if sys.platform == "linux":  # Only for Raspberry Pi
    import lirc
###########################################################################
import configparser
import pygame
import pygame.locals

from exceptions import ExceptionFormat, ExceptionNotFound
from modules.BlockBase import BlockBase

class BlockIR(BlockBase):
    """description of class"""

    def __init__(self, logger, setting):
        """Initializes (declare internal variables)"""
        super(BlockIR, self).__init__(logger, setting)
###########################################################################
        if sys.platform == "linux":  # Only for Raspberry Pi
            lirc.init("dashboard", "IR.ini", blocking=False)
###########################################################################

    def init(self, modList):
        """Initializes (initialize internal variables)"""
        # Загружаем настройки
        section = self._setting.Configuration["IRBlock"]

        self._voice = modList['Voice'];

        self.updateInfo(True)

    def proccedEvent(self, event, isOnline):
        try:
###########################################################################
            if sys.platform == "linux":  # Only for Raspberry Pi
                code = lirc.nextcode()
            else:
                code = []
###########################################################################
            if len(code) == 0:
                return
            self._voice.execute()

        except Exception as ex:
            self._logger.exception(ex)

    def done(self):
        """ """
###########################################################################
        if sys.platform == "linux":  # Only for Raspberry Pi
            lirc.deinit()
###########################################################################
