import configparser

from exceptions import ExceptionFormat, ExceptionNotFound
from modules.BlockBase import BlockBase
from modules.BlockSecondBase import BlockSecondBase

EXCEPTION_TEXT = "Не заданы блоки для отображения"


class BlockSwap(BlockSecondBase):
    """description of class"""

    def __init__(self, logger, setting):
        """Initializes (declare internal variables)"""
        super(BlockSwap, self).__init__(logger, setting)
        self._blocks = []
        self._index = 0

    def init(self, modList):
        """Initializes (initialize internal variables)"""
        # Загружаем настройки
        section = self._setting.Configuration["SwapBlock"]

        time = section.getint("UpdateTime")
        if time is None:
            raise ExceptionNotFound(section.name, "UpdateTime")

        selection = section.get("BlockList", "")
        selection = [item.strip(" '") for item in selection.split(",") if item.strip()]
        for name in selection:
            if name in modList:
                self.addBlock(modList[name])

        if not self._blocks:
            raise Exception(EXCEPTION_TEXT)
        for block in self._blocks:
            block.init(modList)

        self.setTime(time)
        self.updateInfo(True)

    def proccedEvent(self, event, isOnline):
        for block in self._blocks:
            block.proccedEvent(event, isOnline)
        super(BlockSwap, self).proccedEvent(event, isOnline)

    def updateInfo(self, isOnline):
        self._index = self._index + 1
        if self._index >= len(self._blocks):
            self._index = 0

    def updateDisplay(self, isOnline, screen, size, foreColor, backColor, current_time):
        try:
            if not isOnline:
                return
            block = self._blocks[self._index]
            block.updateDisplay(isOnline, screen, size, foreColor, backColor, current_time)
        except Exception as ex:
            self._logger.exception(ex)

    def getText(self):
        """ """
        block = self._blocks[self._index]
        self._text = block.getText()
        return self._text

    def done(self):
        """ """
        for block in self._blocks:
            block.done()

    def addBlock(self, block):
        """  """
        if not isinstance(block, BlockBase):
            raise("Передаваемый параметр должен быть наследником BlockBase")
        self._blocks.append(block)
