from typing import Dict, Tuple
from configparser import ConfigParser, SectionProxy
from abc import ABCMeta, abstractmethod
from tkinter import LabelFrame


class BaseManager(LabelFrame, metaclass=ABCMeta):
    """" Базовый класс с загрузкой/сохранением для модуля (Manager) """

    @abstractmethod
    def load(self, config: ConfigParser, module_list: Dict[str, 'BaseManager']) -> None:
        """ Загрузка данных модуля из ini файла (ConfigParser) """

    @abstractmethod
    def save(self, config: ConfigParser) -> None:
        """ Сохранение данных модуля в ini файл (ConfigParser) """

    def load_font(self, section: SectionProxy, name: str,
                  font_name_def: str = "Helvetica",
                  font_size_def: int = 32,
                  is_bold_def: bool = False,
                  is_italic_def: bool = False) -> Tuple[str, int, bool, bool]:
        """ Загрузка шрифта """
        if not isinstance(section, SectionProxy):
            raise TypeError("section")
        font_name = section.get(name + "Name", font_name_def)
        font_size = section.getint(name + "Size", font_size_def)
        is_bold = section.getboolean(name + "Bold", is_bold_def)
        is_italic = section.getboolean(name + "Italic", is_italic_def)
        return (font_name, font_size, is_bold, is_italic)
