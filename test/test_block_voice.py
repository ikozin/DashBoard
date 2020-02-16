import pytest
from exceptions import ExceptionNotFound
from setting import Setting
from modules.BlockBase import BlockBase
from modules.block_voice import BlockVoice

SECTION_NAME = "VoiceBlock"


@pytest.mark.block_voice
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


@pytest.mark.block_voice
def test_init_speaker(logger):
    check_property(logger, "", "Speaker")


@pytest.mark.block_voice
def test_init_speed(logger):
    check_property(logger, "Speaker", "Speed")


@pytest.mark.block_voice
def test_init_key(logger):
    check_property(logger, "Speed", "Key")


@pytest.mark.block_voice
def test_init_blocks(logger):
    check_property(logger, "Key", "BlockList")


@pytest.mark.block_voice
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
        "Speed": "1.0",
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


def check_property(logger, settingPropName, propName):
    config = _get_setting(settingPropName)
    block = BlockTime(logger, config)
    assert block is not None
    with pytest.raises(ExceptionNotFound) as err_not_found:
        block.init({})
    assert err_not_found.value.config_name == SECTION_NAME
    assert err_not_found.value.param_name == propName
