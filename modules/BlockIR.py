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

CONFIG_FILE_NMAE = "IR.ini"
PROG_NAME = "dashboard"


class BlockIR(BlockBase):
    """description of class"""

    def __init__(self, logger, setting):
        """Initializes (declare internal variables)"""
        super(BlockIR, self).__init__(logger, setting)

    def init(self, modList):
        """Initializes (initialize internal variables)"""
        # Загружаем настройки
        section = self._setting.Configuration["IRBlock"]
        keyList = dict()
        for keyCode in section:
            keyList[keyCode.upper()] = section.get(keyCode)
        with open(CONFIG_FILE_NMAE, "w", encoding="utf-8") as file:
            for keyCode in keyList.keys():
                file.write("begin\n\tprog={1}\n\tbutton={0}\n\tconfig={0}\n\trepeat=0\nend\n".format(keyCode, PROG_NAME))
###########################################################################
        if sys.platform == "linux":  # Only for Raspberry Pi
            lirc.init(PROG_NAME, CONFIG_FILE_NMAE, blocking=False)
###########################################################################

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
