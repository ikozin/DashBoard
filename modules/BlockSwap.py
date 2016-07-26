import configparser 
import pygame
import pygame.locals

from datetime  import datetime, timedelta
from exceptions import ExceptionFormat, ExceptionNotFound
from modules.BlockBase import BlockBase

BLOCK_SWAP_UPDATE_EVENT = (pygame.locals.USEREVENT + 6)
EXCEPTION_TEXT = "Не заданы блоки для отображения"

class BlockSwap(BlockBase):
    """description of class"""

    def __init__(self, logger, setting):
        """Initializes (declare internal variables)"""
        super(BlockSwap, self).__init__(logger, setting)
        self._lastSwap = datetime.now()
        self._needUpdate = True
        self._showBlock1 = True
        self._block1 = None
        self._block2 = None


    def init(self, fileName):
        """Initializes (initialize internal variables)"""
        #config = configparser.ConfigParser()
        #config.read(fileName, "utf-8")
        #section = config["SwapBlock"]
        if not self._block1: raise Exception(EXCEPTION_TEXT)
        if not self._block2: raise Exception(EXCEPTION_TEXT)
        self._block1.init(fileName)
        self._block2.init(fileName)
        pygame.time.set_timer(BLOCK_SWAP_UPDATE_EVENT, 10000)


    def proccedEvent(self, event, isOnline):
        self._block1.proccedEvent(event, isOnline)
        self._block2.proccedEvent(event, isOnline)
        if event.type == BLOCK_SWAP_UPDATE_EVENT: self.updateInfo(isOnline)


    def updateInfo(self, isOnline):
        if self._needUpdate:
            self._block1.updateInfo(isOnline)
            self._block2.updateInfo(isOnline)
        self._needUpdate = False
        self._showBlock1 = not self._showBlock1


    def updateDisplay(self, isOnline, screen, size, foreColor, backColor):
        try:
            if not isOnline: return
            if self._showBlock1:
                self._block1.updateDisplay(isOnline, screen, size, foreColor, backColor)
            else:
                self._block2.updateDisplay(isOnline, screen, size, foreColor, backColor)
        except Exception as ex:
            self._logger.exception(ex)


    def getText(self):
        """ """
        if self._showBlock1:
            self._text = self._block1.getText()
        else:
            self._text = self._block2.getText()
        return self._text


    def AddBlocks(self, block1, block2):
        if not isinstance(block1, BlockBase): raise("Передаваемый параметр block1 должен быть наследником BlockBase")
        if not isinstance(block2, BlockBase): raise("Передаваемый параметр block2 должен быть наследником BlockBase")
        self._block1 = block1
        self._block2 = block2
