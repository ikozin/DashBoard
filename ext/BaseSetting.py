from abc import ABCMeta, abstractclassmethod
from tkinter import ttk

class BaseSetting(ttk.LabelFrame, metaclass=ABCMeta):

    @abstractclassmethod
    def load(self, config, sectionName):
        pass

    @abstractclassmethod
    def pre_save(self):
        pass

    @abstractclassmethod
    def save(self, config, sectionName):
        pass

    @abstractclassmethod
    def rename(self, sectionName):
        pass

