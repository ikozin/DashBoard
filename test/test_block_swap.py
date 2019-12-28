import pytest
from setting import Setting
from modules.BlockBase import BlockBase
from modules.block_swap import BlockSwap

# SECTION_NAME = "SwapBlock"


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
