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
def test_block_ir_execute(logger, mocker):
    config = _get_setting(None)
    block = BlockIR(logger, config, Lirc_Stub)
    assert block is not None
    assert isinstance(block, BlockBase)

    mock_block = mocker.patch('modules.BlockBase.BlockBase', spec=True)
    inst = mock_block.return_value
    inst.execute.return_value = None
    block.init({"Swap": inst, "Voice": inst})

    inst.execute.reset_mock()
    block.execute()  # "key_0": "Voice",
    block.execute()  # "key_1": "Voice",
    block.execute()  # "key_2": "Voice",
    block.execute()  # "key_3": "Voice",
    block.execute()  # "key_4": "Voice",
    block.execute()  # "key_5": "Voice",
    block.execute()  # "key_6": "Voice",
    block.execute()  # "key_7": "Voice",
    block.execute()  # "key_8": "Voice",
    block.execute()  # "key_9": "Voice",
    assert inst.execute.call_count == 10

    inst.execute.reset_mock()
    block.execute()  # "key_channeldown": "Swap,-1",
    inst.execute.assert_called_once_with("-1")

    inst.execute.reset_mock()
    block.execute()  # "key_channelup": "Swap,1"
    inst.execute.assert_called_once_with("1")

    inst.execute.reset_mock()
    block.execute("KEY")
    inst.execute.assert_not_called()


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
    block.execute()  # "key_0": "Voice",
    inst.execute.assert_called_once()


def _get_setting(name):
    params = {
        "key_0": "Voice,",
        "key_1": "Voice,",
        "key_2": "Voice,",
        "key_3": "Voice,",
        "key_4": "Voice,",
        "key_5": "Voice,",
        "key_6": "Voice,",
        "key_7": "Voice,",
        "key_8": "Voice,",
        "key_9": "Voice,",
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
        self._key_list = [
            "KEY_0",
            "KEY_1",
            "KEY_2",
            "KEY_3",
            "KEY_4",
            "KEY_5",
            "KEY_6",
            "KEY_7",
            "KEY_8",
            "KEY_9",
            "KEY_CHANNELDOWN",
            "KEY_CHANNELUP"]
        self._index = 0

    def getCode(self, code: str = None) -> str:
        code = self._key_list[self._index]
        self._index = self._index + 1
        self._index = self._index % len(self._key_list)
        return code
