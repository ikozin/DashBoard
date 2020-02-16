import pytest
from setting import Setting
from modules.BlockBase import BlockBase
from modules.block_open_weathermap import BlockOpenWeatherMap

SECTION_NAME = "OpenWeatherMapBlock"


@pytest.mark.block_openweathermap
def test_block_openweathermap(logger):
    config = Setting()
    with pytest.raises(TypeError):
        BlockOpenWeatherMap(None, None)
    with pytest.raises(TypeError):
        BlockOpenWeatherMap(None, config)
    with pytest.raises(TypeError):
        BlockOpenWeatherMap(logger, None)
    block = BlockOpenWeatherMap(logger, config)
    assert block is not None
    assert isinstance(block, BlockBase)
    with pytest.raises(KeyError):
        block.init({})
