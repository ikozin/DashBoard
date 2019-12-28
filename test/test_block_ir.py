import pytest
from logging import Logger
import pygame
from setting import Setting
from modules.BlockBase import BlockBase
from modules.block_ir import BlockIR

# SECTION_NAME = "IRBlock"


@pytest.fixture(scope='module', autouse=True)
def procced():
    pygame.font.init()
    yield


@pytest.fixture(scope='module')
def logger():
    return Logger("Log")


def test_block_ir(logger):
    config = Setting()
    with pytest.raises(TypeError):
        BlockIR(None, None)
    with pytest.raises(TypeError):
        BlockIR(None, config)
    with pytest.raises(TypeError):
        BlockIR(logger, None)
    block = BlockIR(logger, config)
    assert block is not None
    assert isinstance(block, BlockBase)
    with pytest.raises(KeyError):
        block.init({})
