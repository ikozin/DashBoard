import sys
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
        self._moduleList = modList
        for keyCode in section:
            self._list[keyCode.upper()] = section.get(keyCode)
            moduleName = self._list[keyCode.upper()].split(",")[0]
            if moduleName not in self._moduleList:
                raise ExceptionNotFound(section.name, keyCode.upper())
        with open(CONFIG_FILE_NMAE, "w", encoding="utf-8") as file:
            for keyCode in self._list.keys():
                file.write("begin\n\tprog={1}\n\tbutton={0}\n\tconfig={0}\n\trepeat=0\nend\n".format(keyCode, PROG_NAME))
        self.module_init()
        # self.updateInfo(True)

    def proccedEvent(self, event, isOnline):
        self.execute()

    def execute(self, *args):
        try:
            code = args[0] if len(args) == 1 else self.module_getcode()
            if len(code) == 0:
                return
            keyCode = code[0]
            if keyCode not in self._list:
                return
            values = self._list[keyCode].split(",")
            if values[0] in self._moduleList:
                if (len(values) == 2):
                    self._moduleList[values[0]].execute(values[1])
                else:
                    self._moduleList[values[0]].execute()

        except Exception as ex:
            self._logger.exception(ex)

    def done(self):
        """ """
        self.module_done()


###########################################################################
    if sys.platform == "linux":  # Only for Raspberry Pi
        import lirc

        def module_init(self):
            lirc.init(PROG_NAME, CONFIG_FILE_NMAE, blocking=False)

        def module_done(self):
            lirc.deinit()

        def module_getcode(self, code=None):
            code = lirc.nextcode()
            return code

    else:
        def module_init(self):
            pass

        def module_done(self):
            pass

        def module_getcode(self, code=[]):
            return code
###########################################################################
