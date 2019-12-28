import pytest
from logging import Logger
import pygame
from setting import Setting
from modules.BlockBase import BlockBase
from modules.block_watcher import BlockWatcher

SECTION_NAME = "WatcherBlock"


@pytest.fixture(scope='module', autouse=True)
def procced():
    pygame.font.init()
    yield

@pytest.fixture(scope='module')
def logger():
    return Logger("Log");

def test_block_watcher(logger):
    config = Setting()
    with pytest.raises(TypeError):
        BlockWatcher(None, None)
    with pytest.raises(TypeError):
        BlockWatcher(None, config)
    with pytest.raises(TypeError):
        BlockWatcher(logger, None)
    block = BlockWatcher(logger, config)
    assert block is not None
    assert isinstance(block, BlockBase)
    with pytest.raises(KeyError):
        block.init({})
