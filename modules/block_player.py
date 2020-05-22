from typing import Dict, Any
from modules.BlockBase import BlockBase
from logging import Logger
from setting import Setting

import pygame


class BlockPlayer(BlockBase):
    """description of class"""

    def __init__(self, logger: Logger, setting: Setting):
        """Initializes (declare internal variables)"""
        super(BlockPlayer, self).__init__(logger, setting)

    def init(self, mod_list: Dict[str, BlockBase]) -> None:
        """Initializes (initialize internal variables)"""

    def execute(self, *args) -> Any:
        fileName = None
        if len(args) == 1:
            fileName = args[0]

        if fileName:
            pygame.mixer.music.load(fileName)
            pygame.mixer.music.play()
