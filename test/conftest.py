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
