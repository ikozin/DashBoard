import datetime
import configparser
import pygame
import pygame.locals

from exceptions import ExceptionFormat, ExceptionNotFound
from modules.BlockBase import BlockBase
from modules.alarm.BlockAlarmSimple import BlockAlarmSimple
from modules.alarm.BlockAlarmBlink import BlockAlarmBlink
from modules.alarm.BlockAlarmRise import BlockAlarmRise
from modules.alarm.BlockAlarmExecute import BlockAlarmExecute

BLOCK_ALARM_UPDATE_EVENT = (pygame.locals.USEREVENT + 4)


class BlockAlarm(BlockBase):
    """description of class"""

    def __init__(self, logger, setting):
        """Initializes (declare internal variables)"""
        super(BlockAlarm, self).__init__(logger, setting)
        self._blocks = []
        self._alarmBlock = []
        self._functions = {1: BlockAlarmSimple, 2: BlockAlarmBlink, 3: BlockAlarmRise, 4: BlockAlarmExecute}

    def init(self, modList):
        """Initializes (initialize internal variables)"""
        # Загружаем настройки
        section = self._setting.Configuration["AlarmBlock"]

        selection = section.get("BlockList", "")
        selection = [item.strip(" '") for item in selection.split(",") if item.strip()]
        for name in selection:
            if name in modList:
                self.addBlock(modList[name])

        csvValue = section.get("List")
        if csvValue is None:
            return

        alarmSchemas = [item.strip(" '") for item in csvValue.split(",") if item.strip()]
        for schema in alarmSchemas:
            if not self._setting.Configuration.has_section(schema):
                raise Exception("Ошибка конфигурации! Нет секции [{0}]".format(schema))

            section = self._setting.Configuration[schema]
            type = section.getint("Type")
            if type is None:
                raise ExceptionNotFound(schema, "Type")

            func = self._functions.get(type, None)
            if func is None:
                raise ExceptionFormat(schema, "Type")
            alarm = func(self._logger, self._setting)
            alarm.init(section, modList)
            self._alarmBlock.append(alarm)

        pygame.time.set_timer(BLOCK_ALARM_UPDATE_EVENT, 500)
        self.updateInfo(True)

    def proccedEvent(self, event, isOnline):
        if event.type == BLOCK_ALARM_UPDATE_EVENT:
            self.updateInfo(isOnline)

    def updateInfo(self, isOnline):
        try:
            if not self._alarmBlock:
                return
            value = datetime.datetime.now()
            for item in self._alarmBlock:
                item.updateState(value)
        except Exception as ex:
            self._logger.exception(ex)

    def updateDisplay(self, isOnline, screen, size, foreColor, backColor, current_time):
        try:
            if not self._alarmBlock:
                return
            for item in self._alarmBlock:
                item.updateDisplay(screen, size, foreColor, backColor, self._blocks, current_time)
        except Exception as ex:
            self._logger.exception(ex)

    def addBlock(self, block):
        if not isinstance(block, BlockBase):
            raise TypeError("Передаваемый параметр должен быть наследником BlockBase")
        self._blocks.append(block)
