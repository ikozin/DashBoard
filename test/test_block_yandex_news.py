import pytest
from logging import Logger
import pygame
from setting import Setting
from modules.BlockBase import BlockBase
from modules.block_yandex_news import BlockYandexNews

SECTION_NAME = "YandexNewsBlock"


@pytest.fixture(scope='module', autouse=True)
def procced():
    pygame.font.init()
    yield


@pytest.fixture(scope='module')
def logger():
    return Logger("Log")


def test_block_yandex_news(logger):
    config = Setting()
    with pytest.raises(TypeError):
        BlockYandexNews(None, None)
    with pytest.raises(TypeError):
        BlockYandexNews(None, config)
    with pytest.raises(TypeError):
        BlockYandexNews(logger, None)
    block = BlockYandexNews(logger, config)
    assert block is not None
    assert isinstance(block, BlockBase)
    with pytest.raises(KeyError):
        block.init({})
