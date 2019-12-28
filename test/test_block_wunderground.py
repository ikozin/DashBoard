import pytest
from logging import Logger
import pygame
from setting import Setting
from modules.BlockBase import BlockBase
from modules.block_wunderground import BlockWunderGround

SECTION_NAME = "WunderGroundBlock"


def test_block_wunderground(logger):
    config = Setting()
    with pytest.raises(TypeError):
        BlockWunderGround(None, None)
    with pytest.raises(TypeError):
        BlockWunderGround(None, config)
    with pytest.raises(TypeError):
        BlockWunderGround(logger, None)
    block = BlockWunderGround(logger, config)
    assert block is not None
    assert isinstance(block, BlockBase)
    with pytest.raises(KeyError):
        block.init({})
