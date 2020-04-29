from .lirc_base import Lirc_Base
from logging import Logger

from lirc import RawConnection

class Lirc_RaspPi(Lirc_Base):
    """description of class"""

    def __init__(self, logger: Logger):
        """Initializes (declare internal variables)"""
        super(Lirc_Base, self).__init__(logger)
        self._conn = RawConnection()

    def getCode(self, code: str=None) -> str:
        try:
            # 000000000000000f 00 KEY_3 carmp3
            keypress = self._conn.readline(.0001)
        except:
            keypress=""            
        if (keypress != "" and keypress != None):
            data = keypress.split()
            sequence = data[1]
            command = data[2]
            if (sequence == "00"):
                return command
        return None
