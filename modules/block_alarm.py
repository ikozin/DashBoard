import datetime

import time
import configparser 
import pygame
import pygame.locals

from block_base import BlockBase
from setting import TEXT_EXCEPTION_NOT_FOUND

BLOCK_ALARM_UPDATE_EVENT  = (pygame.locals.USEREVENT + 5)
BLOCK_ALARM_RESET_EVENT   = (pygame.locals.USEREVENT + 6)
BLOCK_ALARM_ANIMATE_EVENT = (pygame.locals.USEREVENT + 7)

class BlocklAlarm(BlockBase):
    """description of class"""

    def __init__(self, logger):
        """Initializes (declare internal variables)"""
        super(BlocklAlarm, self).__init__(logger)
        self._blocks = []
        self._alarmList = []
        self._time = None

        self._isAlarm = False
        self._alarm = False
        self._counter = None


    def init(self, fileName):
        """Initializes (initialize internal variables)"""
        # Загружаем настройки
        config = configparser.ConfigParser()
        config.read(fileName, "utf-8")

        section = config["AlarmBlock"]
        if section is None: return
        list = section.get("List")
        if list is None: return
        alarmSchemas = [item.strip(" '") for item in list.split(",") if item.strip()]
        for schema in alarmSchemas:
            if not config.has_section(schema):
                raise Exception("Ошибка конфигурации! Нет секции [{0}]".format(schema))
            section = config[schema]
            alarmTime = section.get("Time")
            if not alarmTime:
                raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(schema, "Time"))
            alarmTime = time.strptime(alarmTime, "%H:%M:%S")
            type = section.getint("Type")
            if type is None:      raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(schema, "Type"))
            if type == 1:
                duration = section.getint("Duration")
                foreColor = self._getTuple(section.get("ForegroudColor"))
                backColor = self._getTuple(section.get("BackgroudColor"))

                if duration is None:  raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(schema, "Duration"))
                if foreColor is None: raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(schema, "ForegroudColor"))
                if backColor is None: raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(schema, "BackgroudColor"))

                if len(foreColor) != 3: raise Exception(TEXT_EXCEPTION_FORMAT.format(schema, "ForegroudColor"))
                if len(backColor) != 3: raise Exception(TEXT_EXCEPTION_FORMAT.format(schema, "BackgroudColor"))

                # --------------------------------------------
                # формат кортежа
                # --------------------------------------------
                # Time - время активации (для всех типов)
                # Type - тип анимации (для всех типов)
                # --------------------------------------------
                # Duration - длительность анимации в секундах
                # ForegroudColor - цвет текста
                # BackgroudColor - цвет фона
                # --------------------------------------------
                self._alarmList.append((alarmTime, type, duration, foreColor, backColor))
            #elif type == 2:
            #    duration = section.getint("Duration")
            #    foreColor = self._getTuple(section.get("ForegroudColor"))
            #    backColor = self._getTuple(section.get("BackgroudColor"))

            #    if duration is None:  raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(schema, "Duration"))
            #    if foreColor is None: raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(schema, "ForegroudColor"))
            #    if backColor is None: raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(schema, "BackgroudColor"))

            #    if len(foreColor) != 3: raise Exception(TEXT_EXCEPTION_FORMAT.format(schema, "ForegroudColor"))
            #    if len(backColor) != 3: raise Exception(TEXT_EXCEPTION_FORMAT.format(schema, "BackgroudColor"))

            #    # --------------------------------------------
            #    # формат кортежа
            #    # --------------------------------------------
            #    # Time - время активации (для всех типов)
            #    # Type - тип анимации (для всех типов)
            #    # --------------------------------------------
            #    # Duration - длительность анимации в секундах
            #    # ForegroudColor - цвет текста
            #    # BackgroudColor - цвет фона
            #    # --------------------------------------------
            else: raise Exception(TEXT_EXCEPTION_FORMAT.format(schema, "Type"))

        #list.sort(self._list, key=lambda entry: entry[0])
        pygame.time.set_timer(BLOCK_ALARM_UPDATE_EVENT, 500)


    def proccedEvent(self, event, isOnline):
        if event.type == BLOCK_ALARM_UPDATE_EVENT:
            self.updateInfo(isOnline)
        if event.type == BLOCK_ALARM_RESET_EVENT:
            self.alarmReset()
        if event.type == BLOCK_ALARM_ANIMATE_EVENT:
            self.alarmAnimate()


    def updateInfo(self, isOnline):
        try:
            if not self._alarmList: return

            value = time.localtime()
            for alarmItem in self._alarmList:
                alarmTime = alarmItem[0]
                if value.tm_hour == alarmTime.tm_hour:
                    if value.tm_min == alarmTime.tm_min:
                        if value.tm_sec == alarmTime.tm_sec:
                            self._isAlarm = True
                            if self._alarm != alarmItem:
                                self._counter = 0;
                                self._alarm = alarmItem
                                if self._alarm[1] == 1:
                                    pygame.time.set_timer(BLOCK_ALARM_RESET_EVENT, self._alarm[2] * 1000)
                                else:
                                    pass
                                #print(self._alarm)
        except Exception as ex:
            self._logger.exception(ex)


    def updateDisplay(self, isOnline, screen, size, foreColor, backColor):
        try:
            if not self._isAlarm: return
            if self._alarm[1] == 1:
                screen.fill(self._alarm[4])
                for block in self._blocks:
                    block.updateDisplay(True, screen, size, self._alarm[3], self._alarm[4])
            #elif self._alarm[1] == 2:
            #    pass
            else:
                pass

        except Exception as ex:
            self._logger.exception(ex)

    def alarmReset(self):
        pygame.time.set_timer(BLOCK_ALARM_ANIMATE_EVENT, 0)
        self._isAlarm = False


    def alarmAnimate(self):
    #    if self._alarm[1] == 1:
    #        pass
    #    elif self._alarm[1] == 2:
    #        pygame.time.set_timer(BLOCK_ALARM_ANIMATE_EVENT, 100)
    #    else:
    #        pass
        pass


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
