# https://habr.com/ru/post/448782/ - Python Testing с pytest. Начало работы с pytest, Глава 1
# https://habr.com/ru/post/448788/ - Python Testing с pytest. Глава 2, Написание тестовых функций
# https://habr.com/ru/post/448786/ - Python Testing с pytest. ГЛАВА 3 pytest Fixtures
# https://habr.com/ru/post/448792/ - Python Testing с pytest. Builtin Fixtures, Глава 4
# https://habr.com/ru/post/448794/ - Python Testing с pytest. Плагины, ГЛАВА 5
# https://habr.com/ru/post/448796/ - Python Testing с pytest. Конфигурация, ГЛАВА 6
# https://habr.com/ru/post/448798/ - Python Testing с pytest. Использование pytest с другими инструментами, ГЛАВА 7
# https://habr.com/ru/post/269759/ - PyTest
import pytest
from logging import Logger
import pygame


@pytest.fixture(scope='module', autouse=True)
def procced():
    pygame.init()
    pygame.font.init()
    yield


@pytest.fixture(scope='module')
def logger():
    return Logger("Log")
