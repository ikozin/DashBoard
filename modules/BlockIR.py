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
        self._moduleList = None
        self._list = None

    def init(self, modList):
        """Initializes (initialize internal variables)"""
        # Загружаем настройки
        section = self._setting.Configuration["IRBlock"]
        self._list = dict()
        for keyCode in section:
            self._list[keyCode.upper()] = section.get(keyCode)
        with open(CONFIG_FILE_NMAE, "w", encoding="utf-8") as file:
            for keyCode in self._list.keys():
                file.write("begin\n\tprog={1}\n\tbutton={0}\n\tconfig={0}\n\trepeat=0\nend\n".format(keyCode, PROG_NAME))
        self._moduleList = modList
###########################################################################
        if sys.platform == "linux":  # Only for Raspberry Pi
            lirc.init(PROG_NAME, CONFIG_FILE_NMAE, blocking=False)
###########################################################################
        #self.updateInfo(True)

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
            keyCode = code[0]
            if keyCode not in self._list:
                return
            values = self._list[keyCode].split(",")
            self._moduleList[values[0]].execute()

        except Exception as ex:
            self._logger.exception(ex)

    def done(self):
        """ """
###########################################################################
        if sys.platform == "linux":  # Only for Raspberry Pi
            lirc.deinit()
###########################################################################
