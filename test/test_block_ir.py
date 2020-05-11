import pytest
from setting import Setting
from modules.BlockBase import BlockBase
from modules.block_ir import BlockIR
from logging import Logger
from modules.hal.lirc_base import Lirc_Base

SECTION_NAME = "IRBlock"


@pytest.mark.block_ir
def test_block_ir(logger, mocker):
    config = Setting()
    with pytest.raises(TypeError):
        BlockIR(None, None, None)
    with pytest.raises(TypeError):
        BlockIR(None, config, None)
    with pytest.raises(TypeError):
        BlockIR(logger, None, None)
    block = BlockIR(logger, config, Lirc_Stub)
    assert block is not None
    assert isinstance(block, BlockBase)
    with pytest.raises(KeyError):
        block.init({})


@pytest.mark.block_ir
def test_block_ir_exec_NO_KEY(logger, mocker):
    config = _get_setting(None)

    block = BlockIR(logger, config, Lirc_Stub)
    assert block is not None
    assert isinstance(block, BlockBase)

    mock_block = mocker.patch('modules.BlockBase.BlockBase', spec=True)
    inst = mock_block.return_value
    block.init({"Block": inst})
    block.execute("NO_KEY")
    inst.execute.assert_not_called()


@pytest.mark.block_ir
def test_block_ir_exec_KEY(logger, mocker):
    config = _get_setting(None)

    mocker.patch.object(Lirc_Stub, 'getCode', return_value="KEY")
    block = BlockIR(logger, config, Lirc_Stub)
    assert block is not None
    assert isinstance(block, BlockBase)

    mock_block = mocker.patch('modules.BlockBase.BlockBase', spec=True)
    inst = mock_block.return_value
    block.init({"Block": inst})
    block.execute()
    inst.execute.assert_called_once_with()


@pytest.mark.block_ir
def test_block_ir_exec_KEY_PARAM(logger, mocker):
    config = _get_setting(None)

    mocker.patch.object(Lirc_Stub, 'getCode', return_value="KEY_PARAM")
    block = BlockIR(logger, config, Lirc_Stub)
    assert block is not None
    assert isinstance(block, BlockBase)

    mock_block = mocker.patch('modules.BlockBase.BlockBase', spec=True)
    inst = mock_block.return_value
    block.init({"Block": inst})
    block.execute()
    inst.execute.assert_called_once_with("parameter")


def _get_setting(params):
    if not params:
        params = {
            "KEY": "Block,",
            "KEY_PARAM": "Block,parameter",
        }
    config = Setting()
    config.configuration.add_section(SECTION_NAME)
    section = config.configuration[SECTION_NAME]
    for key, value in params.items():
        section[key] = value.__str__()
    return config


class Lirc_Stub(Lirc_Base):
    """description of class"""

    def __init__(self, logger: Logger):
        """Initializes (declare internal variables)"""
        super(Lirc_Stub, self).__init__(logger)

    def getCode(self, code: str = None) -> str:
        pass
