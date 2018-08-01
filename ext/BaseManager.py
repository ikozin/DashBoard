import configparser
from abc import ABCMeta, abstractclassmethod
from tkinter import ttk


class BaseManager(ttk.LabelFrame, metaclass=ABCMeta):

    @abstractclassmethod
    def load(self, config, modulelist):
        pass

    @abstractclassmethod
    def save(self, config):
        pass

    def loadFont(self, section, name, fontNameDef = "Helvetica", fontSizeDef = 32, isBoldDef = False, isItalicDef = False):
        if not isinstance(section, configparser.SectionProxy):
            raise TypeError("section")
        fontName = section.get(name + "Name", fontNameDef)
        fontSize = section.getint(name + "Size", fontSizeDef)
        isBold = section.getboolean(name + "Bold", isBoldDef)
        isItalic = section.getboolean(name + "Italic", isItalicDef)
        return (fontName, fontSize, isBold, isItalic)
