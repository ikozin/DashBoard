from block_base import BlockBase

class BlockTextAgregator(BlockBase):
    """description of class"""

    def __init__(self, logger, setting):
        """Initializes (declare internal variables)"""
        super(BlockTextAgregator, self).__init__(logger, setting)
        self._blocks = []


    def addBlock(self, block):
        """ Добавляем источник текстового сообщения """
        if not isinstance(block, BlockBase):
            raise("Передаваемый параметр должен быть наследником BlockBase")
        self._blocks.append(block)


    def getText(self):
        """ Формируем текстовое сообщение из добавленных источников"""
        self._text = ". ".join(map(lambda block: block.getText(), self._blocks))
        return self._text
