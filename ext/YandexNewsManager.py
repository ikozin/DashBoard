import configparser

from tkinter import *
from tkinter import font
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import colorchooser

class YandexNewsManager(ttk.LabelFrame):
    """description of class"""

    def __init__(self, root):
        """ """
        super(YandexNewsManager, self).__init__(root, text="Настройки новостей от Яндекса")

    def load(self, config):
        if not isinstance(config, configparser.ConfigParser): raise TypeError("config")
        section = config["YandexNewsBlock"]

    def save(self, config):
        if not isinstance(config, configparser.ConfigParser): raise TypeError("config")
        if not config.has_section("YandexNewsBlock"):      config.add_section("YandexNewsBlock")
        section = config["YandexNewsBlock"]
