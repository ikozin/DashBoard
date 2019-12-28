import pytest
from logging import Logger
import pygame
from exceptions import ExceptionNotFound
from setting import Setting
from modules.BlockBase import BlockBase


@pytest.fixture(scope='module', autouse=True)
def procced():
    pygame.font.init()
    yield


@pytest.fixture(scope='module')
def logger():
    return Logger("Log")


#@pytest.fixture
#def block_create(TypeBlock):
#    config = Setting()
#    with pytest.raises(TypeError):
#        TypeBlock(None, None)
#    with pytest.raises(TypeError):
#        TypeBlock(None, config)
#    with pytest.raises(TypeError):
#        TypeBlock(logger, None)
#    block = TypeBlock(logger, config)
#    assert block is not None
#    assert isinstance(block, BlockBase)
#    with pytest.raises(KeyError):
#        block.init({})
