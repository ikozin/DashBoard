from typing import *

from configparser import ConfigParser, SectionProxy
from abc import ABCMeta, abstractclassmethod
from tkinter import LabelFrame


class BaseManager(LabelFrame, metaclass=ABCMeta):

    @abstractclassmethod
    def load(self, config: ConfigParser, modulelist: Dict[str, 'BaseManager']) -> None:
        pass

    @abstractclassmethod
    def save(self, config: ConfigParser) -> None:
        pass

    def loadFont(self, section: SectionProxy, name: str,
                 fontNameDef: str = "Helvetica", fontSizeDef: int = 32,
                 isBoldDef: bool = False, isItalicDef: bool = False) -> Tuple[str, int, bool, bool]:
        if not isinstance(section, SectionProxy):
            raise TypeError("section")
        fontName = section.get(name + "Name", fontNameDef)
        fontSize = section.getint(name + "Size", fontSizeDef)
        isBold = section.getboolean(name + "Bold", isBoldDef)
        isItalic = section.getboolean(name + "Italic", isItalicDef)
        return (fontName, fontSize, isBold, isItalic)
