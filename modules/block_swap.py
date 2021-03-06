from typing import Dict, Any
from exceptions import ExceptionNotFound
from modules.BlockBase import BlockBase
from modules.BlockSecondBase import BlockSecondBase
from logging import Logger
from setting import Setting

EXCEPTION_TEXT = "Не заданы блоки для отображения"


class BlockSwap(BlockSecondBase):
    """description of class"""

    def __init__(self, logger: Logger, setting: Setting):
        """Initializes (declare internal variables)"""
        super(BlockSwap, self).__init__(logger, setting)
        self._blocks = []
        self._index = 0

    def init(self, mod_list: Dict[str, BlockBase]) -> None:
        """Initializes (initialize internal variables)"""
        # Загружаем настройки
        section = self._setting.configuration["SwapBlock"]

        time = section.getint("UpdateTime")
        if time is None:
            raise ExceptionNotFound(section.name, "UpdateTime")

        selection = section.get("BlockList", fallback="")
        if not selection:
            raise ExceptionNotFound(section.name, "BlockList")

        selection = [item.strip(" '") for item in selection.split(",") if item.strip()]
        for name in selection:
            if name in mod_list:
                self.add_block(mod_list[name])

        if not self._blocks:
            raise Exception(EXCEPTION_TEXT)
        for block in self._blocks:
            try:
                block.init(mod_list)
            except Exception as ex:
                self._logger.exception(ex)

        self.set_time(time)
        # self.update_info(True)

    def procced_event(self, event, is_online: bool) -> None:
        for block in self._blocks:
            block.procced_event(event, is_online)
        super(BlockSwap, self).procced_event(event, is_online)

    def update_info(self, is_online):
        self.execute()

    def update_display(self, is_online: bool, screen, size, fore_color, back_color, current_time) -> None:
        try:
            if not is_online:
                return
            block = self._blocks[self._index]
            block.update_display(is_online, screen, size, fore_color, back_color, current_time)
        except Exception as ex:
            self._logger.exception(ex)

    def execute(self, *args) -> Any:
        value = int(args[0]) if len(args) == 1 else 1
        self._index += value
        self._index %= len(self._blocks)

    def get_text(self) -> str:
        block = self._blocks[self._index]
        self._text = block.get_text()
        return self._text

    def done(self) -> None:
        for block in self._blocks:
            block.done()

    def add_block(self, block: BlockBase) -> None:
        if not isinstance(block, BlockBase):
            raise TypeError("Передаваемый параметр должен быть наследником BlockBase")
        self._blocks.append(block)
