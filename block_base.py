class BlockBase:
    """description of class"""

    def __init__(self, logger):
        """Ininitializes"""
        self._logger = logger
        self._text = None

    def __del__(self):
        """Destructor"""
        pass


    def init(self, fileName):
        """ """
        pass


    def proccedEvent(self, event, isOnline):
        """ """
        pass


    def updateInfo(self, isOnline):
        """ """
        if not isOnline: return
        pass

    
    def updateDisplay(self, isOnline, screen, size, foreColor, backColor):
        """ """
        pass


    def getText(self):
        """ """
        return self._text
