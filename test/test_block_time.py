import pytest
from logging import Logger
from exceptions import ExceptionNotFound
import pygame
from setting import Setting
from modules.BlockBase import BlockBase
from modules.block_time import BlockTime

SECTION_NAME = "TimeBlock"


@pytest.fixture(scope='module', autouse=True)
def procced():
    pygame.font.init()
    yield


@pytest.fixture(scope='module')
def logger():
    return Logger("Log")


def test_block_time(logger):
    config = Setting()
    with pytest.raises(TypeError):
        BlockTime(None, None)
    with pytest.raises(TypeError):
        BlockTime(None, config)
    with pytest.raises(TypeError):
        BlockTime(logger, None)
    block = BlockTime(logger, config)
    assert block is not None
    assert isinstance(block, BlockBase)
    with pytest.raises(KeyError):
        block.init({})


def test_init_font_name(logger):
    config = _get_setting("")
    block = BlockTime(logger, config)
    assert block is not None
    with pytest.raises(ExceptionNotFound) as err_not_found:
        block.init({})
    assert err_not_found.value.config_name == SECTION_NAME
    assert err_not_found.value.param_name == "FontName"


def test_init_font_size(logger):
    config = _get_setting("FontName")
    block = BlockTime(logger, config)
    assert block is not None
    with pytest.raises(ExceptionNotFound) as err_not_found:
        block.init({})
    assert err_not_found.value.config_name == SECTION_NAME
    assert err_not_found.value.param_name == "FontSize"


def test_init_font_bold(logger):
    config = _get_setting("FontSize")
    block = BlockTime(logger, config)
    assert block is not None
    with pytest.raises(ExceptionNotFound) as err_not_found:
        block.init({})
    assert err_not_found.value.config_name == SECTION_NAME
    assert err_not_found.value.param_name == "FontBold"


def test_init_font_italic(logger):
    config = _get_setting("FontBold")
    block = BlockTime(logger, config)
    assert block is not None
    with pytest.raises(ExceptionNotFound) as err_not_found:
        block.init({})
    assert err_not_found.value.config_name == SECTION_NAME
    assert err_not_found.value.param_name == "FontItalic"


def test_init(logger):
    config = _get_setting(None)
    block = BlockTime(logger, config)
    assert block is not None
    block.init({})
    assert block._font is not None
    assert block._time is None


def test_execute(logger):
    config = _get_setting(None)
    block = BlockTime(logger, config)
    assert block is not None
    block.init({})
    block.execute()
    assert block._text is not None
    assert block._time is None


def test_get_text(logger):
    config = _get_setting(None)
    block = BlockTime(logger, config)
    assert block is not None
    block.init({})
    text = block.get_text()
    assert text is not None
    assert block._text is not None
    assert block._time is None


def _get_setting(name):
    params = {
        "FontName": "Helvetica",
        "FontSize": 384,
        "FontBold": True,
        "FontItalic": False,
    }
    config = Setting()
    config.configuration.add_section(SECTION_NAME)
    if name == "":
        return config
    section = config.configuration[SECTION_NAME]
    for key, value in params.items():
        section[key] = value.__str__()
        if key == name:
            break
    return config
