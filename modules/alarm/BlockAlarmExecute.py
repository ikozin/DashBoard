import configparser
import datetime

from modules.alarm.AlarmTimeBase import AlarmTimeBase


class BlockAlarmExecute(AlarmTimeBase):
    """description of class"""

    def __init__(self, logger, setting):
        """Initializes (declare internal variables)"""
        super(BlockAlarmExecute, self).__init__(logger, setting)
        self._isAlarm = False

    def init(self, configSection, modList):
        """Initializes (initialize internal variables)"""
        super(BlockAlarmExecute, self).init(configSection, modList)
        self._modList = modList
        self._module = configSection.get("Module")

    def updateDisplay(self, screen, size, foreColor, backColor, blocks, current_time):
        try:
            if not self._isAlarm:
                return
            screen.fill(backColor)
            for block in blocks:
                block.updateDisplay(True, screen, size, foreColor, backColor, current_time)

        except Exception as ex:
            self._logger.exception(ex)

    def execute(self):
        if self._isAlarm: return
        self._isAlarm = True
        self._modList[self._module].execute()
