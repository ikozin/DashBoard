import pytest
from logging import Logger
import pygame
from setting import Setting
from modules.BlockBase import BlockBase
from modules.block_yandex_weather import BlockYandexWeather

SECTION_NAME = "YandexWeatherBlock"


@pytest.fixture(scope='module', autouse=True)
def procced():
    pygame.font.init()
    yield


@pytest.fixture(scope='module')
def logger():
    return Logger("Log")


def test_block_yandex_weather(logger):
    config = Setting()
    with pytest.raises(TypeError):
        BlockYandexWeather(None, None)
    with pytest.raises(TypeError):
        BlockYandexWeather(None, config)
    with pytest.raises(TypeError):
        BlockYandexWeather(logger, None)
    block = BlockYandexWeather(logger, config)
    assert block is not None
    assert isinstance(block, BlockBase)
    with pytest.raises(KeyError):
        block.init({})
