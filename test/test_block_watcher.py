import pytest
from exceptions import ExceptionNotFound
from setting import Setting
from modules.BlockBase import BlockBase
from modules.block_watcher import BlockWatcher

SECTION_NAME = "WatcherBlock"


@pytest.mark.block_watcher
def test_block_watcher(logger):
    config = Setting()
    with pytest.raises(TypeError):
        BlockWatcher(None, None)
    with pytest.raises(TypeError):
        BlockWatcher(None, config)
    with pytest.raises(TypeError):
        BlockWatcher(logger, None)
    block = BlockWatcher(logger, config)
    assert block is not None
    assert isinstance(block, BlockBase)
    with pytest.raises(KeyError):
        block.init({})


@pytest.mark.block_watcher
def test_init_weekday(logger):
    check_property(logger, "", "Weekday")


@pytest.mark.block_watcher
def test_init_start_time(logger):
    check_property(logger, "Weekday", "StartTime")


@pytest.mark.block_watcher
def test_init_finish_time(logger):
    check_property(logger, "StartTime", "FinishTime")


@pytest.mark.block_watcher
def test_init_update_time(logger):
    check_property(logger, "FinishTime", "UpdateTime")


@pytest.mark.block_watcher
def test_init_path(logger):
    check_property(logger, "UpdateTime", "Path")


def _get_setting(name):
    params = {
        "Weekday": "0, 1, 2, 3, 4",
        "StartTime": "09:00:00",
        "FinishTime": "19:00:00",
        "UpdateTime": 60,
        "Path": "bash /home/pi/DashBoard/webcam.sh"
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
    block = BlockWatcher(logger, config)
    assert block is not None
    with pytest.raises(ExceptionNotFound) as err_not_found:
        block.init({})
    assert err_not_found.value.config_name == SECTION_NAME
    assert err_not_found.value.param_name == propName


