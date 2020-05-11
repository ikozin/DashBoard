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
def test_block_ir_exec(logger, mocker):
    config = _get_setting(None)
    block = BlockIR(logger, config, Lirc_Stub)
    assert block is not None
    assert isinstance(block, BlockBase)

    mock_block = mocker.patch('modules.BlockBase.BlockBase', spec=True)
    inst = mock_block.return_value
    inst.execute.return_value = None
    block.init({"Swap": inst, "Voice": inst})

    block.execute("KEY")
    inst.execute.assert_not_called()


@pytest.mark.block_ir
def test_block_ir_exec_KEY_0(logger, mocker, monkeypatch):
    config = _get_setting(None)
    
    mocker.patch.object(Lirc_Stub, 'getCode', return_value="KEY_0")
    block = BlockIR(logger, config, Lirc_Stub)
    assert block is not None
    assert isinstance(block, BlockBase)

    mock_block = mocker.patch('modules.BlockBase.BlockBase', spec=True)
    inst = mock_block.return_value
    inst.execute.return_value = None
    block.init({"Swap": None, "Voice": inst})
    block.execute()  # "key_0": "Voice",
    inst.execute.assert_called_once_with()


@pytest.mark.block_ir
def test_block_ir_exec_KEY_1(logger, mocker, monkeypatch):
    config = _get_setting(None)
    
    mocker.patch.object(Lirc_Stub, 'getCode', return_value="KEY_1")
    block = BlockIR(logger, config, Lirc_Stub)
    assert block is not None
    assert isinstance(block, BlockBase)

    mock_block = mocker.patch('modules.BlockBase.BlockBase', spec=True)
    inst = mock_block.return_value
    inst.execute.return_value = None
    block.init({"Swap": None, "Voice": inst})
    block.execute()  # "key_1": "Voice,parameter",
    inst.execute.assert_called_once_with("parameter")


@pytest.mark.block_ir
def test_block_ir_exec_KEY_CHANNELDOWN(logger, mocker, monkeypatch):
    config = _get_setting(None)
    
    mocker.patch.object(Lirc_Stub, 'getCode', return_value="KEY_CHANNELDOWN")
    block = BlockIR(logger, config, Lirc_Stub)
    assert block is not None
    assert isinstance(block, BlockBase)

    mock_block = mocker.patch('modules.BlockBase.BlockBase', spec=True)
    inst = mock_block.return_value
    inst.execute.return_value = None
    block.init({"Swap": inst, "Voice": None})
    block.execute()  # "key_channeldown": "Swap,-1",
    inst.execute.assert_called_once_with("-1")


@pytest.mark.block_ir
def test_block_ir_exec_KEY_CHANNELUP(logger, mocker, monkeypatch):
    config = _get_setting(None)
    
    mocker.patch.object(Lirc_Stub, 'getCode', return_value="KEY_CHANNELUP")
    block = BlockIR(logger, config, Lirc_Stub)
    assert block is not None
    assert isinstance(block, BlockBase)

    mock_block = mocker.patch('modules.BlockBase.BlockBase', spec=True)
    inst = mock_block.return_value
    inst.execute.return_value = None
    block.init({"Swap": inst, "Voice": None})
    block.execute()  # "key_channelup": "Swap,1"
    inst.execute.assert_called_once_with("1")


def _get_setting(name):
    params = {
        "key_0": "Voice,",
        "key_1": "Voice,parameter",
        "key_channeldown": "Swap,-1",
        "key_channelup": "Swap,1"
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


class Lirc_Stub(Lirc_Base):
    """description of class"""

    def __init__(self, logger: Logger):
        """Initializes (declare internal variables)"""
        super(Lirc_Stub, self).__init__(logger)

    def getCode(self, code: str = None) -> str:
        pass