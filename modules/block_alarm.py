import datetime
import configparser 
import pygame
import pygame.locals

from block_base import BlockBase
from exceptions import ExceptionFormat, ExceptionNotFound

from modules.alarm.block_alarm_simple import BlockAlarmSimple
from modules.alarm.block_alarm_blink import BlockAlarmBlink
from modules.alarm.block_alarm_rise import BlockAlarmRise

BLOCK_ALARM_UPDATE_EVENT  = (pygame.locals.USEREVENT + 5)

class BlocklAlarm(BlockBase):
    """description of class"""

    def __init__(self, logger, setting):
        """Initializes (declare internal variables)"""
        super(BlocklAlarm, self).__init__(logger, setting)
        self._blocks = []
        self._alarmBlock = []


    def init(self, fileName):
        """Initializes (initialize internal variables)"""
        # Загружаем настройки
        config = configparser.ConfigParser()
        config.read(fileName, "utf-8")

        section = config["AlarmBlock"]
        if section is None: return

        csvValue = section.get("List")
        if csvValue is None: return

        alarmSchemas = [item.strip(" '") for item in csvValue.split(",") if item.strip()]
        for schema in alarmSchemas:
            if not config.has_section(schema):
                raise Exception("Ошибка конфигурации! Нет секции [{0}]".format(schema))

            section = config[schema]
            type = section.getint("Type")
            if type is None: raise ExceptionNotFound(schema, "Type")

            if type == 1:
                alarm = BlockAlarmSimple(self._logger, self._setting)
            elif type == 2:
                alarm = BlockAlarmBlink(self._logger, self._setting)
            elif type == 3:
                alarm = BlockAlarmRise(self._logger, self._setting)
            else:
                raise ExceptionFormat(schema, "Type")
            alarm.init(section)
            self._alarmBlock.append(alarm)

        pygame.time.set_timer(BLOCK_ALARM_UPDATE_EVENT, 500)


    def proccedEvent(self, event, isOnline):
        if event.type == BLOCK_ALARM_UPDATE_EVENT:
            self.updateInfo(isOnline)


    def updateInfo(self, isOnline):
        try:
            if not self._alarmBlock: return
            value = datetime.datetime.now()
            for item in self._alarmBlock:
                item.updateState(value)
        except Exception as ex:
            self._logger.exception(ex)


    def updateDisplay(self, isOnline, screen, size, foreColor, backColor):
        try:
            if not self._alarmBlock: return
            value = datetime.datetime.now()
            for item in self._alarmBlock:
                item.updateDisplay(screen, size, foreColor, backColor, self._blocks)
        except Exception as ex:
            self._logger.exception(ex)


    def addBlock(self, block):
        if not isinstance(block, BlockBase):
            raise("Передаваемый параметр должен быть наследником BlockBase")
        self._blocks.append(block)


    def _getTuple(self, value):
        """ Конвертирует строку '0, 0, 0' в кортеж (0, 0, 0) """
        try:
            return tuple(int(item.strip("([ '])")) for item in value.split(",") if item.strip())
        except Exception as ex:
            self._logger.exception(ex)
            return None
