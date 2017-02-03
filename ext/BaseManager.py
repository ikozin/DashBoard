from abc import ABCMeta, abstractclassmethod
from tkinter import ttk


class BaseManager(ttk.LabelFrame, metaclass=ABCMeta):

    @abstractclassmethod
    def load(self, config, modulelist):
        pass

    @abstractclassmethod
    def save(self, config):
        pass
