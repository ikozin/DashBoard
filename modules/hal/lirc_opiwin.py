from .lirc_base import Lirc_Base
from logging import Logger


class Lirc_OraPiWin(Lirc_Base):
    """description of class"""

    def __init__(self, logger: Logger):
        """Initializes (declare internal variables)"""
        super(Lirc_OraPiWin, self).__init__(logger)

    def getCode(self, code: str = None) -> str:
        return code
