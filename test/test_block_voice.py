import pytest
from logging import Logger
from exceptions import ExceptionNotFound
import pygame
from setting import Setting
from modules.BlockBase import BlockBase
from modules.block_voice import BlockVoice

SECTION_NAME = "VoiceBlock"


@pytest.fixture(scope='module', autouse=True)
def procced():
    pygame.font.init()
    yield


@pytest.fixture(scope='module')
def logger():
    return Logger("Log")


def test_block_voice(logger):
    config = Setting()
    with pytest.raises(TypeError):
        BlockVoice(None, None)
    with pytest.raises(TypeError):
        BlockVoice(None, config)
    with pytest.raises(TypeError):
        BlockVoice(logger, None)
    block = BlockVoice(logger, config)
    assert block is not None
    assert isinstance(block, BlockBase)
    with pytest.raises(KeyError):
        block.init({})

def test_init_speaker(logger):
    config = _get_setting("")
    block = BlockVoice(logger, config)
    assert block is not None
    with pytest.raises(ExceptionNotFound) as err_not_found:
        block.init({})
    assert err_not_found.value.config_name == SECTION_NAME
    assert err_not_found.value.param_name == "Speaker"

def test_init_key(logger):
    config = _get_setting("Speaker")
    block = BlockVoice(logger, config)
    assert block is not None
    with pytest.raises(ExceptionNotFound) as err_not_found:
        block.init({})
    assert err_not_found.value.config_name == SECTION_NAME
    assert err_not_found.value.param_name == "Key"

def test_init_blocks(logger):
    config = _get_setting("Key")
    block = BlockVoice(logger, config)
    assert block is not None
    with pytest.raises(ExceptionNotFound) as err_not_found:
        block.init({})
    assert err_not_found.value.config_name == SECTION_NAME
    assert err_not_found.value.param_name == "BlockList"

def test_init(logger):
    config = _get_setting(None)
    block = BlockVoice(logger, config)
    assert block is not None
    block.init({"Voice": block})
    assert block._speaker is not None
    assert block._key is not None
    assert block._speed is not None
    assert block._blocks is not None
    assert block in block._blocks
    assert len(block._blocks) == 1

def _get_setting(name):
    params = {
        "Speaker": "omazh",
        "Key": "b55d97e9-6c66-4e1b-966f-c2a6aa9d939d",
        "BlockList": "Voice",
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
