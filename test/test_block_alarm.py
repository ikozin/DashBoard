import pytest
from setting import Setting
from modules.BlockBase import BlockBase
from modules.block_alarm import BlockAlarm

SECTION_NAME = "AlarmBlock"


def test_block_alarm(logger):
    config = Setting()
    with pytest.raises(TypeError):
        BlockAlarm(None, None)
    with pytest.raises(TypeError):
        BlockAlarm(None, config)
    with pytest.raises(TypeError):
        BlockAlarm(logger, None)
    block = BlockAlarm(logger, config)
    assert block is not None
    assert isinstance(block, BlockBase)
    with pytest.raises(KeyError):
        block.init({})

def test_init(logger):
    config = _get_setting(None)
    block = BlockAlarm(logger, config)
    assert block is not None
    block.init({})
    assert block._blocks is not None
    assert block._alarm_block is not None
    assert block._functions is not None


def _get_setting(name):
    params = {
        "BlockList": "Time",
        "List": "",
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
