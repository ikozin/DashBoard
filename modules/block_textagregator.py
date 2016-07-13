import configparser 
import pygame
import pygame.locals

from block_base import BlockBase

class BlockTextAgregator(BlockBase):
    """description of class"""

    def __init__(self, logger):
        """Ininitializes"""
        super(BlockTextAgregator, self).__init__(logger)
        self._blocks = []


    def init(self, fileName):
        """ """
        # Загружаем настройки
        config = configparser.ConfigParser()
        config.read(fileName, encoding="utf-8")


    def addBlock(self, block):
        """ """
        if not isinstance(block, BlockBase):
            raise("Передаваемы парамтр должен быть наследником BlockBase")
        self._blocks.append(block)


    def getText(self):
        """ """
        self._text = ". ".join(map(lambda block: block.getText(), self._blocks))
        return self._text
