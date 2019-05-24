from configparser import ConfigParser
from abc import ABCMeta, abstractmethod
from tkinter import LabelFrame


class BaseSetting(LabelFrame, metaclass=ABCMeta):
    """ Базовый класс с загрузкой/сохранением для секции модуля (Timeline, будильники) """

    @abstractmethod
    def load(self, config: ConfigParser, section_name: str) -> None:
        """ Загрузка данных секции """

    @abstractmethod
    def pre_save(self) -> None:
        """ Подготовка к сохранению секции """

    @abstractmethod
    def save(self, config: ConfigParser, section_name: str) -> None:
        """ Сохранение данных секции """

    @abstractmethod
    def rename(self, section_name: str) -> None:
        """ Переименование секции """
