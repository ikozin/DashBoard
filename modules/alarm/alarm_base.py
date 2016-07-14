import configparser 

class AlarmBase:
    """description of class"""

    def __init__(self, logger):
        """Initializes (declare internal variables)"""
        self._logger = logger

    def __del__(self):
        """Destructor"""
        pass

    def init(self, configSection):
        """Initializes (initialize internal variables)"""
        if not isinstance(configSection, configparser.SectionProxy):
            raise("Передаваемый параметр должен быть наследником configparser.SectionProxy")


    def updateState(self, currentTime):
        pass


    def updateDisplay(self, screen, size, foreColor, backColor, blocks):
        pass

    def _getTuple(self, value):
        """ Конвертирует строку '0, 0, 0' в кортеж (0, 0, 0) """
        try:
            return tuple(int(item.strip("([ '])")) for item in value.split(",") if item.strip())
        except Exception as ex:
            self._logger.exception(ex)
            return None
