from typing import *

from configparser import ConfigParser
from abc import ABCMeta, abstractclassmethod
from tkinter import LabelFrame


class BaseSetting(LabelFrame, metaclass=ABCMeta):

    @abstractclassmethod
    def load(self, config: ConfigParser, sectionName: str) -> None:
        pass

    @abstractclassmethod
    def pre_save(self):
        pass

    @abstractclassmethod
    def save(self, config: ConfigParser, sectionName: str) -> None:
        pass

    @abstractclassmethod
    def rename(self, sectionName: str) -> None:
        pass
