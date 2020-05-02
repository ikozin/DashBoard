from .lirc_base import Lirc_Base
from logging import Logger

import socket


class Lirc_RaspPi(Lirc_Base):
    """description of class"""

    def __init__(self, logger: Logger):
        """Initializes (declare internal variables)"""
        super(Lirc_Base, self).__init__(logger)
        self._sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self._sock.setblocking(0)
        self._sock.connect("/var/run/lirc/lircd")

    def __del__(self):
        """Destructor"""
        self._sock.close()

    def getCode(self, code: str=None) -> str:
        try:
            data = self._sock.recv(128)
            data = data.strip()
            if data:
                words = data.split()
                return words[2].decode("utf-8")
        except:
            pass
        return None
