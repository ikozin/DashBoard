from abc import ABCMeta, abstractclassmethod
from logging import Logger
from setting import Setting

from modules.BlockBase import BlockBase


class BlockExecuteBase(BlockBase):
    """description of class"""

    def __init__(self, logger, setting):
        """Initializes (declare internal variables)"""
        super(BlockExecuteBase, self).__init__(logger, setting)

    def init(self, fileName, isOnline, modList):
        """Initializes (initialize internal variables)"""
        pass

    @abstractclassmethod
    def execute(self):
        """ """
        pass
