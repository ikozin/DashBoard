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


@pytest.mark.block_mt8057
def test_init_format_warn(logger, mocker):
    mocker.patch("modules.block_mt8057.MT8057", spec=True)
    check_property(logger, "", "Warn")


@pytest.mark.block_mt8057
def test_init_format_crit(logger, mocker):
    mocker.patch("modules.block_mt8057.MT8057", spec=True)
    check_property(logger, "Warn", "Crit")


@pytest.mark.block_mt8057
def test_init_format_warn_color(logger, mocker):
    mocker.patch("modules.block_mt8057.MT8057", spec=True)
    check_property(logger, "Crit", "WarnColor")


@pytest.mark.block_mt8057
def test_init_format_crit_color(logger, mocker):
    mocker.patch("modules.block_mt8057.MT8057", spec=True)
    check_property(logger, "WarnColor", "CritColor")


@pytest.mark.block_mt8057
def test_init_format_co2_text(logger, mocker):
    mocker.patch("modules.block_mt8057.MT8057", spec=True)
    check_property(logger, "CritColor", "CO2Text")


@pytest.mark.block_mt8057
def test_init_format_co2_font_name(logger, mocker):
    mocker.patch("modules.block_mt8057.MT8057", spec=True)
    check_property(logger, "CO2Text", "CO2FontName")


@pytest.mark.block_mt8057
def test_init_format_co2_font_size(logger, mocker):
    mocker.patch("modules.block_mt8057.MT8057", spec=True)
    check_property(logger, "CO2FontName", "CO2FontSize")


@pytest.mark.block_mt8057
def test_init_format_co2_font_bold(logger, mocker):
    mocker.patch("modules.block_mt8057.MT8057", spec=True)
    check_property(logger, "CO2FontSize", "CO2FontBold")


@pytest.mark.block_mt8057
def test_init_format_co2_font_italic(logger, mocker):
    mocker.patch("modules.block_mt8057.MT8057", spec=True)
    check_property(logger, "CO2FontBold", "CO2FontItalic")


@pytest.mark.block_mt8057
def test_init_format_co2_pos(logger, mocker):
    mocker.patch("modules.block_mt8057.MT8057", spec=True)
    check_property(logger, "CO2FontItalic", "CO2Pos")


@pytest.mark.block_mt8057
def test_init_format_co2_align_x(logger, mocker):
    mocker.patch("modules.block_mt8057.MT8057", spec=True)
    check_property(logger, "CO2Pos", "CO2AlignX")


@pytest.mark.block_mt8057
def test_init_format_co2_align_y(logger, mocker):
    mocker.patch("modules.block_mt8057.MT8057", spec=True)
    check_property(logger, "CO2AlignX", "CO2AlignY")


@pytest.mark.block_mt8057
def test_init_format_temp_text(logger, mocker):
    mocker.patch("modules.block_mt8057.MT8057", spec=True)
    check_property(logger, "CO2AlignY", "TempText")


@pytest.mark.block_mt8057
def test_init_format_temp_font_name(logger, mocker):
    mocker.patch("modules.block_mt8057.MT8057", spec=True)
    check_property(logger, "TempText", "TempFontName")


@pytest.mark.block_mt8057
def test_init_format_temp_font_size(logger, mocker):
    mocker.patch("modules.block_mt8057.MT8057", spec=True)
    check_property(logger, "TempFontName", "TempFontSize")


@pytest.mark.block_mt8057
def test_init_format_temp_font_bold(logger, mocker):
    mocker.patch("modules.block_mt8057.MT8057", spec=True)
    check_property(logger, "TempFontSize", "TempFontBold")


@pytest.mark.block_mt8057
def test_init_format_temp_font_italic(logger, mocker):
    mocker.patch("modules.block_mt8057.MT8057", spec=True)
    check_property(logger, "TempFontBold", "TempFontItalic")


@pytest.mark.block_mt8057
def test_init_format_temp_pos(logger, mocker):
    mocker.patch("modules.block_mt8057.MT8057", spec=True)
    check_property(logger, "TempFontItalic", "TempPos")


@pytest.mark.block_mt8057
def test_init_format_temp_align_x(logger, mocker):
    mocker.patch("modules.block_mt8057.MT8057", spec=True)
    check_property(logger, "TempPos", "TempAlignX")


@pytest.mark.block_mt8057
def test_init_format_temp_align_y(logger, mocker):
    mocker.patch("modules.block_mt8057.MT8057", spec=True)
    check_property(logger, "TempAlignX", "TempAlignY")


@pytest.mark.block_mt8057
def test_init_format_format_text(logger, mocker):
    mocker.patch("modules.block_mt8057.MT8057", spec=True)
    check_property(logger, "TempAlignY", "FormatText")


def _get_setting(name):
    params = {
        "Warn": 800,
        "Crit": 1200,
        "WarnColor": (255, 255, 0),
        "CritColor": (255, 63, 63),
        "CO2Text": "Концентрация CO2: {0}",
        "CO2FontName": "Helvetica",
        "CO2FontSize": 140,
        "CO2FontBold": True,
        "CO2FontItalic": False,
        "CO2Pos": (960, 200),
        "CO2AlignX": "Center",
        "CO2AlignY": "Center",
        "TempText": "",
        "TempFontName": "Helvetica",
        "TempFontSize": 140,
        "TempFontBold": True,
        "TempFontItalic": False,
        "TempPos": (0, 0),
        "TempAlignX": "Left",
        "TempAlignY": "Top",
        "FormatText": "Концентрация CO2: {0}.Температура: {1:+.1f}."
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
