import pytest
from exceptions import ExceptionNotFound
from setting import Setting
from modules.BlockBase import BlockBase
from modules.block_calendar import BlockCalendar

SECTION_NAME = "CalendarBlock"


@pytest.mark.block_calendar
def test_block_calendar(logger):
    config = Setting()
    with pytest.raises(TypeError):
        BlockCalendar(None, None)
    with pytest.raises(TypeError):
        BlockCalendar(None, config)
    with pytest.raises(TypeError):
        BlockCalendar(logger, None)
    block = BlockCalendar(logger, config)
    assert block is not None
    assert isinstance(block, BlockBase)
    with pytest.raises(KeyError):
        block.init({})


@pytest.mark.block_calendar
def test_init_font_name(logger):
    check_property(logger, "", "FontName")


@pytest.mark.block_calendar
def test_init_font_size(logger):
    check_property(logger, "FontName", "FontSize")


@pytest.mark.block_calendar
def test_init_font_bold(logger):
    check_property(logger, "FontSize", "FontBold")


@pytest.mark.block_calendar
def test_init_font_italic(logger):
    check_property(logger, "FontBold", "FontItalic")


@pytest.mark.block_calendar
def test_init_position(logger):
    check_property(logger, "FontItalic", "Position")


@pytest.mark.block_calendar
def test_init_format(logger):
    check_property(logger, "Position", "Format")


@pytest.mark.block_calendar
def test_init_format_text(logger):
    check_property(logger, "Format", "FormatText")


@pytest.mark.block_calendar
def test_init(logger):
    config = _get_setting(None)
    block = BlockCalendar(logger, config)
    assert block is not None
    block.init({})

    assert block._days_long is not None
    assert block._months is not None
    assert block._weekday_shot is not None
    assert len(block._weekday_shot) == 7
    assert block._weekday_long is not None
    assert len(block._weekday_long) == 7
    assert block._font is not None
    assert block._pos is not None
    assert block._time is None
    assert block._format_date is None
    assert block._format is None


@pytest.mark.block_calendar
def test_execute(logger):
    config = _get_setting(None)
    block = BlockCalendar(logger, config)
    assert block is not None
    block.init({})
    block.execute()
    assert block._text is not None
    assert block._time is None


def test_get_text(logger):
    config = _get_setting(None)
    block = BlockCalendar(logger, config)
    assert block is not None
    block.init({})
    text = block.get_text()
    assert text is not None
    assert block._text is not None
    assert block._time is None


def _get_setting(name):
    params = {
        "FontName": "Helvetica",
        "FontSize": 170,
        "FontBold": True,
        "FontItalic": False,
        "Position": 80,
        "Format": "{3} {0} {1} {2}",
        "FormatText": "{4}, {0} {1} {2} год"
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
    block = BlockCalendar(logger, config)
    assert block is not None
    with pytest.raises(ExceptionNotFound) as err_not_found:
        block.init({})
    assert err_not_found.value.config_name == SECTION_NAME
    assert err_not_found.value.param_name == propName
