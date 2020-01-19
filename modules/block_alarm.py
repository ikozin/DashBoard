import datetime
import pygame
import pygame.locals

from exceptions import ExceptionFormat, ExceptionNotFound
from modules.BlockBase import BlockBase
from modules.alarm.block_alarm_simple import BlockAlarmSimple
from modules.alarm.block_alarm_blink import BlockAlarmBlink
from modules.alarm.block_alarm_rise import BlockAlarmRise
from modules.alarm.block_alarm_execute import BlockAlarmExecute
from modules.alarm.block_alarm_text import BlockAlarmText
from logging import Logger
from setting import Setting

BLOCK_ALARM_UPDATE_EVENT = (pygame.locals.USEREVENT + 4)


class BlockAlarm(BlockBase):
    """description of class"""

    def __init__(self, logger: Logger, setting: Setting):
        """Initializes (declare internal variables)"""
        super(BlockAlarm, self).__init__(logger, setting)
        self._blocks = []
        self._alarm_block = []
        self._functions = {1: BlockAlarmSimple, 2: BlockAlarmBlink, 3: BlockAlarmRise, 4: BlockAlarmExecute, 5: BlockAlarmText}

    def init(self, mod_list) -> None:
        """Initializes (initialize internal variables)"""
        # Загружаем настройки
        section = self._setting.configuration["AlarmBlock"]

        selection = section.get("BlockList", "")
        selection = [item.strip(" '") for item in selection.split(",") if item.strip()]
        for name in selection:
            if name in mod_list:
                self.add_block(mod_list[name])

        csv_value = section.get("List")
        if csv_value is None:
            return

        alarm_schemas = [item.strip(" '") for item in csv_value.split(",") if item.strip()]
        for schema in alarm_schemas:
            if not self._setting.configuration.has_section(schema):
                raise Exception("Ошибка конфигурации! Нет секции [{0}]".format(schema))

            section = self._setting.configuration[schema]
            alarm_type = section.getint("Type")
            if alarm_type is None:
                raise ExceptionNotFound(schema, "Type")

            func = self._functions.get(alarm_type, None)
            if func is None:
                raise ExceptionFormat(schema, "Type")
            alarm = func(self._logger, self._setting)
            alarm.init(section, mod_list)
            self._alarm_block.append(alarm)

        pygame.time.set_timer(BLOCK_ALARM_UPDATE_EVENT, 500)
        self.update_info(True)

    def procced_event(self, event, is_online: bool) -> None:
        if event.type == BLOCK_ALARM_UPDATE_EVENT:
            self.update_info(is_online)

    def update_info(self, is_online):
        try:
            if not self._alarm_block:
                return
            value = datetime.datetime.now()
            for item in self._alarm_block:
                item.update_state(value)
        except Exception as ex:
            self._logger.exception(ex)

    def update_display(self, is_online: bool, screen, size, fore_color, back_color, current_time) -> None:
        try:
            if not self._alarm_block:
                return
            for item in self._alarm_block:
                item.update_display(screen, size, fore_color, back_color, self._blocks, current_time)
        except Exception as ex:
            self._logger.exception(ex)

    def add_block(self, block: BlockBase) -> None:
        if not isinstance(block, BlockBase):
            raise TypeError("Передаваемый параметр должен быть наследником BlockBase")
        self._blocks.append(block)
