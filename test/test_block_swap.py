import pytest
from exceptions import ExceptionNotFound
from setting import Setting
from modules.BlockBase import BlockBase
from modules.block_swap import BlockSwap

SECTION_NAME = "SwapBlock"


@pytest.mark.block_swap
def test_block_swap(logger):
    config = Setting()
    with pytest.raises(TypeError):
        BlockSwap(None, None)
    with pytest.raises(TypeError):
        BlockSwap(None, config)
    with pytest.raises(TypeError):
        BlockSwap(logger, None)
    block = BlockSwap(logger, config)
    assert block is not None
    assert isinstance(block, BlockBase)
    with pytest.raises(KeyError):
        block.init({})


@pytest.mark.block_swap
def test_init_update_time(logger):
    check_property(logger, "", "UpdateTime")


# @pytest.mark.block_swap
# def test_init_block_list(logger):
#     check_property(logger, "UpdateTime", "BlockList")


def _get_setting(name):
    params = {
        "UpdateTime": 5,
        "BlockList": "Swap"
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
    block = BlockSwap(logger, config)
    assert block is not None
    with pytest.raises(ExceptionNotFound) as err_not_found:
        block.init({"Swap": block})
    assert err_not_found.value.config_name == SECTION_NAME
    assert err_not_found.value.param_name == propName
