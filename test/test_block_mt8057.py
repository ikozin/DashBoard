import pytest
from logging import Logger
import pygame
from setting import Setting
from modules.BlockBase import BlockBase
from modules.block_mt8057 import BlockMT8057

# SECTION_NAME = "MT8057Block"


def test_block_mt8057(logger):
    config = Setting()
    with pytest.raises(TypeError):
        BlockMT8057(None, None)
    with pytest.raises(TypeError):
        BlockMT8057(None, config)
    with pytest.raises(TypeError):
        BlockMT8057(logger, None)
    block = BlockMT8057(logger, config)
    assert block is not None
    assert isinstance(block, BlockBase)
    with pytest.raises(KeyError):
        block.init({})
