import pytest
from logging import Logger
import pygame
from setting import Setting
from modules.BlockBase import BlockBase
from modules.block_alarm import BlockAlarm


@pytest.fixture(scope='module', autouse=True)
def procced():
    pygame.font.init()
    yield

@pytest.fixture(scope='module')
def logger():
    return Logger("Log");

@pytest.mark.block_alarm
def test_block_alarm(logger):
    config = Setting()
    with pytest.raises(TypeError):
        BlockAlarm(None, None)
    with pytest.raises(TypeError):
        BlockAlarm(None, config)
    with pytest.raises(TypeError):
        BlockAlarm(logger, None)
    block = BlockAlarm(logger, config)
    assert block != None
    assert isinstance(block, BlockBase)

    with pytest.raises(KeyError):
        block.init({})
