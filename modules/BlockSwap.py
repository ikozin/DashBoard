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
        self._blocks = []
        self._index = 0
        self._lastSwap = datetime.now()
        self._time = None


    def init(self, fileName, isOnline, modList):
        """Initializes (initialize internal variables)"""
        config = configparser.ConfigParser()
        config.read(fileName, "utf-8")
        section = config["SwapBlock"]
        self._time = section.getint("UpdateTime")
        selection = section.get("BlockList", "")
        selection = [item.strip(" '") for item in selection.split(",") if item.strip()]
        for name in selection:
            if name in modList:
                self.addBlock(modList[name])

        if not self._blocks: raise Exception(EXCEPTION_TEXT)
        for block in self._blocks:
            block.init(fileName, isOnline, modList)

        pygame.time.set_timer(BLOCK_SWAP_UPDATE_EVENT, self._time * 1000)
        self.updateInfo(isOnline)


    def proccedEvent(self, event, isOnline):
        for block in self._blocks:
            block.proccedEvent(event, isOnline)
        if event.type == BLOCK_SWAP_UPDATE_EVENT: self.updateInfo(isOnline)


    def updateInfo(self, isOnline):
        self._index = self._index + 1
        if self._index >= len(self._blocks):
            self._index = 0

    def updateDisplay(self, isOnline, screen, size, foreColor, backColor):
        try:
            if not isOnline: return
            block = self._blocks[self._index]
            block.updateDisplay(isOnline, screen, size, foreColor, backColor)
        except Exception as ex:
            self._logger.exception(ex)


    def getText(self):
        """ """
        block = self._blocks[self._index]
        self._text = block.getText()
        return self._text

    def addBlock(self, block):
        """  """
        if not isinstance(block, BlockBase):
            raise("Передаваемый параметр должен быть наследником BlockBase")
        self._blocks.append(block)
