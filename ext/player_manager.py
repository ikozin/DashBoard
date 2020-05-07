from typing import Dict
from configparser import ConfigParser
from tkinter import LabelFrame, Label, LEFT
from ext.base_manager import BaseManager


class PlayerManager(BaseManager):
    """description of class"""

    def __init__(self, root: LabelFrame):
        """ """
        super(PlayerManager, self).__init__(root, text="Настройки модуля проигрывателя")
        lbl = Label(self, justify=LEFT, text="Поддерживает следующие команды\n"
                    "<fileName> - имя проигрываемого файла")
        lbl.grid(row=0, column=0, columnspan=2, padx=2, pady=2)

    def load(self, config: ConfigParser, module_list: Dict[str, BaseManager]) -> None:
        if not isinstance(config, ConfigParser):
            raise TypeError("config")

    def save(self, config: ConfigParser) -> None:
        if not isinstance(config, ConfigParser):
            raise TypeError("config")
