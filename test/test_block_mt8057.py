import pytest
from exceptions import ExceptionNotFound
from setting import Setting
from modules.BlockBase import BlockBase
from modules.block_mt8057 import BlockMT8057

SECTION_NAME = "MT8057Block"


@pytest.mark.block_mt8057
def test_block_mt8057(logger):
    config = Setting()
    with pytest.raises(TypeError):
        BlockMT8057(None, None)
    with pytest.raises(TypeError):
        BlockMT8057(None, config)
    with pytest.raises(TypeError):
        BlockMT8057(logger, None)
    block = BlockMT8057(logger, config)
    assert block is not None
    assert isinstance(block, BlockBase)
    with pytest.raises(KeyError):
        block.init({})


def _get_setting(name):
    params = {
        "Warn": 800,
        "Crit": 1200,
        "WarnColor": (255, 255, 0),
        "CritColor": (255, 63, 63),
        "Co2FontName": "Helvetica",
        "Co2FontSize": 100,
        "Co2FontBold": True,
        "Co2FontItalic": False,
        "TempfontName": "Helvetica",
        "TempfontSize": 100,
        "TempfontBold": True,
        "TempfontItalic": False,
        "Co2Pos": (380,32),
        "TempPos": (460,180),
        "Co2Text": "Концентрация CO2: {0}",
        "TemperatureText": "Температура: {1:+.1f}°",
        "FormatText": "Концентрация CO2: {0}.Температура: {1:+.1f}"
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
    block = BlockMT8057(logger, config)
    assert block is not None
    with pytest.raises(ExceptionNotFound) as err_not_found:
        block.init({})
    assert err_not_found.value.config_name == SECTION_NAME
    assert err_not_found.value.param_name == propName
