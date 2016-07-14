import datetime
import configparser 
import pygame
import pygame.locals

from block_base import BlockBase
from setting import TEXT_EXCEPTION_NOT_FOUND

from modules.alarm.block_alarm_simple import BlockAlarmSimple
from modules.alarm.block_alarm_blink import BlockAlarmBlink



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
        self._alarmBlock = []
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
        csvValue = section.get("List")
        if csvValue is None: return
        alarmSchemas = [item.strip(" '") for item in csvValue.split(",") if item.strip()]
        for schema in alarmSchemas:
            if not config.has_section(schema):
                raise Exception("Ошибка конфигурации! Нет секции [{0}]".format(schema))
            section = config[schema]
            type = section.getint("Type")
            if type is None:      raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(schema, "Type"))
            if type == 1:
                alarm = BlockAlarmSimple(self._logger)
                alarm.init(section)
                self._alarmBlock.append(alarm)

                alarmTime = section.get("Time")
                duration = section.getint("Duration")
                foreColor = self._getTuple(section.get("ForegroudColor"))
                backColor = self._getTuple(section.get("BackgroudColor"))

                if alarmTime is None: raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(schema, "Time"))
                if duration is None:  raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(schema, "Duration"))
                if foreColor is None: raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(schema, "ForegroudColor"))
                if backColor is None: raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(schema, "BackgroudColor"))

                if len(foreColor) != 3: raise Exception(TEXT_EXCEPTION_FORMAT.format(schema, "ForegroudColor"))
                if len(backColor) != 3: raise Exception(TEXT_EXCEPTION_FORMAT.format(schema, "BackgroudColor"))

                alarmTime = datetime.datetime.strptime(alarmTime, "%H:%M:%S")

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
                self._alarmList.append({"Time" : alarmTime, 
                                        "Type" : type, 
                                        "Duration" : duration, 
                                        "ForeColor" : foreColor, 
                                        "BackColor" : backColor})
            elif type == 2:
                alarm = BlockAlarmBlink(self._logger)
                alarm.init(section)

                
                alarmTime = section.get("Time")
                duration = section.getint("Duration")
                foreColor = self._getTuple(section.get("ForegroudColor"))
                backColor = self._getTuple(section.get("BackgroudColor"))

                if alarmTime is None: raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(schema, "Time"))
                if duration is None:  raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(schema, "Duration"))
                if foreColor is None: raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(schema, "ForegroudColor"))
                if backColor is None: raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(schema, "BackgroudColor"))

                if len(foreColor) != 3: raise Exception(TEXT_EXCEPTION_FORMAT.format(schema, "ForegroudColor"))
                if len(backColor) != 3: raise Exception(TEXT_EXCEPTION_FORMAT.format(schema, "BackgroudColor"))

                alarmTime = datetime.datetime.strptime(alarmTime, "%H:%M:%S")

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
                self._alarmList.append({"Time" : alarmTime, 
                                        "Type" : type, 
                                        "Duration" : duration, 
                                        "ForeColor" : foreColor, 
                                        "BackColor" : backColor})
            else:
                raise Exception(TEXT_EXCEPTION_FORMAT.format(schema, "Type"))

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

            value = datetime.datetime.now()
            for alarmItem in self._alarmList:
                alarmTime = alarmItem["Time"]
                if (value - alarmTime).seconds == 0:
                    self._isAlarm = True
                    if self._alarm != alarmItem:
                        self._counter = 0
                        self._alarm = alarmItem
                        pygame.time.set_timer(BLOCK_ALARM_RESET_EVENT, self._alarm["Duration"] * 1000)
                        if self._alarm["Type"] == 1:
                            pass
                        elif self._alarm["Type"] == 2:
                            self.alarmAnimate()
                        else:
                            pass
                        #print(self._alarm)
        except Exception as ex:
            self._logger.exception(ex)


    def updateDisplay(self, isOnline, screen, size, foreColor, backColor):
        try:
            if not self._isAlarm: return
            if self._alarm is None: return

            if self._alarm["Type"] == 1:
                screen.fill(self._alarm["BackColor"])
                for block in self._blocks:
                    block.updateDisplay(True, screen, size, self._alarm["ForeColor"], self._alarm["BackColor"])
            elif self._alarm["Type"] == 2:
                if self._counter % 2 == 1:
                    screen.fill(backColor)
                    for block in self._blocks:
                        block.updateDisplay(True, screen, size, self._alarm["ForeColor"], backColor)
                else:
                    screen.fill(self._alarm["BackColor"])
                    for block in self._blocks:
                        block.updateDisplay(True, screen, size, self._alarm["ForeColor"], self._alarm["BackColor"])
            #    pass
            else:
                pass

        except Exception as ex:
            self._logger.exception(ex)

    def alarmReset(self):
        pygame.time.set_timer(BLOCK_ALARM_RESET_EVENT, 0)        
        pygame.time.set_timer(BLOCK_ALARM_ANIMATE_EVENT, 0)
        self._isAlarm = False
        self._alarm = None


    def alarmAnimate(self):
        pygame.time.set_timer(BLOCK_ALARM_ANIMATE_EVENT, 0)
        if self._alarm["Type"] == 1:
            pass
        elif self._alarm["Type"] == 2:
            self._counter += 1
            pygame.time.set_timer(BLOCK_ALARM_ANIMATE_EVENT, 1000)
        else:
            pass
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
