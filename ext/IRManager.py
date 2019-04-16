from typing import *

from configparser import ConfigParser
from tkinter import *

from ext.BaseManager import BaseManager


class IRManager(BaseManager):
    """description of class"""

    def __init__(self, root: LabelFrame):
        """ """
        super(IRManager, self).__init__(root, text="Настройки IR")

    def load(self, config: ConfigParser, modulelist: Dict[str, BaseManager]) -> None:
        if not isinstance(config, ConfigParser):
            raise TypeError("config")
        if not config.has_section("IRBlock"):
            config.add_section("IRBlock")
        section = config["IRBlock"]

    def save(self, config: ConfigParser) -> None:
        if not isinstance(config, ConfigParser):
            raise TypeError("config")
        if not config.has_section("IRBlock"):
            config.add_section("IRBlock")
        section = config["IRBlock"]

