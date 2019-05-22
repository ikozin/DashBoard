from typing import Dict, Tuple, Optional, Union
from configparser import ConfigParser
from tkinter import colorchooser, IntVar, LabelFrame, Label, Entry, Button, N, S, E, W
from ext.base_manager import BaseManager
from ext.modal_dialog import FontChooserFrame, XYFrame


class MT8057Manager(BaseManager):
    """description of class"""

    def __init__(self, root: LabelFrame):
        """ """
        super(MT8057Manager, self).__init__(root, text="Настройки MT8057")
        self._warn_value = IntVar()
        self._crit_value = IntVar()
        self._warn_color = None
        self._crit_color = None

        lbl = Label(self, text="Начальное значения для Предупреждения")
        lbl.grid(row=0, column=0, padx=2, pady=2)

        Entry(self, textvariable=self._warn_value, width=4).grid(row=0, column=1, padx=2, pady=2)

        lbl = Label(self, text="Цвет текста для Предупреждения")
        lbl.grid(row=1, column=0, padx=2, pady=2)

        self._warn_selector = Button(self, text="Предупреждение", command=self._select_warn_color)
        self._warn_selector.grid(row=1, column=1, padx=2, pady=2, sticky=(N, S, E, W))

        lbl = Label(self, text="Начальное значения для Опасности")
        lbl.grid(row=2, column=0, padx=2, pady=2)

        Entry(self, textvariable=self._crit_value, width=4).grid(row=2, column=1, padx=2, pady=2)

        lbl = Label(self, text="Цвет текста для Опасности")
        lbl.grid(row=3, column=0, padx=2, pady=2)

        self._crit_selector = Button(self, text="Опасность", command=self._select_crit_color)
        self._crit_selector.grid(row=3, column=1, padx=2, pady=2, sticky=(N, S, E, W))

        self._pos_co2 = XYFrame(self, "Расположение CO2", "Расположение (X)", "Расположение (Y)")
        self._pos_co2.grid(row=4, column=0, columnspan=2, padx=2, pady=2, sticky=(N, S, E, W))

        self._pos_temp = XYFrame(self, "Расположение Температуры", "Расположение (X)", "Расположение (Y)")
        self._pos_temp.grid(row=5, column=0, columnspan=2, padx=2, pady=2, sticky=(N, S, E, W))

        self._co2 = FontChooserFrame(self, "Параметры шрифта CO2")
        self._co2.grid(row=6, column=0, columnspan=2, padx=2, pady=2, sticky=(N, S, E, W))

        self._temp = FontChooserFrame(self, "Параметры шрифта Температуры")
        self._temp.grid(row=7, column=0, columnspan=2, padx=2, pady=2, sticky=(N, S, E, W))

    def load(self, config: ConfigParser, module_list: Dict[str, BaseManager]) -> None:
        if not isinstance(config, ConfigParser):
            raise TypeError("config")
        if not config.has_section("MT8057Block"):
            config.add_section("MT8057Block")
        section = config["MT8057Block"]
        self._warn_value.set(section.getint("Warn", fallback=800))
        self._crit_value.set(section.getint("Crit", fallback=1200))
        self._warn_color = self._get_tuple(section.get("WarnColor", fallback="(255, 127, 0)"))
        self._crit_color = self._get_tuple(section.get("CritColor", fallback="(255, 63, 63)"))

        font_name = section.get("CO2FontName", fallback="Helvetica")
        font_size = section.getint("CO2FontSize", fallback=100)
        is_bold = section.getboolean("CO2FontBold", fallback=True)
        is_italic = section.getboolean("CO2FontItalic", fallback=False)
        self._co2.load(font_name, font_size, is_bold, is_italic)

        font_name = section.get("TempFontName", fallback="Helvetica")
        font_size = section.getint("TempFontSize", fallback=100)
        is_bold = section.getboolean("TempFontBold", fallback=True)
        is_italic = section.getboolean("TempFontItalic", fallback=False)
        self._temp.load(font_name, font_size, is_bold, is_italic)

        (pos_x, pos_y) = self._get_tuple(section.get("CO2Pos", fallback="(0, 0)"))
        self._pos_co2.load(pos_x, pos_y)
        (pos_x, pos_y) = self._get_tuple(section.get("TempPos", fallback="(0, 0)"))
        self._pos_temp.load(pos_x, pos_y)

        self._warn_selector.configure(foreground="#%02x%02x%02x" % self._warn_color)
        self._crit_selector.configure(foreground="#%02x%02x%02x" % self._crit_color)

    def save(self, config: ConfigParser) -> None:
        if not isinstance(config, ConfigParser):
            raise TypeError("config")
        if not config.has_section("MT8057Block"):
            config.add_section("MT8057Block")
        section = config["MT8057Block"]
        section["Warn"] = str(self._warn_value.get())
        section["Crit"] = str(self._crit_value.get())
        section["WarnColor"] = "(%d, %d, %d)" % self._warn_color
        section["CritColor"] = "(%d, %d, %d)" % self._crit_color

        (font_name, font_size, is_bold, is_italic) = self._co2.get_result()
        section["CO2FontName"] = font_name
        section["CO2FontSize"] = str(font_size)
        section["CO2FontBold"] = str(is_bold)
        section["CO2FontItalic"] = str(is_italic)

        (font_name, font_size, is_bold, is_italic) = self._temp.get_result()
        section["TempFontName"] = font_name
        section["TempFontSize"] = str(font_size)
        section["TempFontBold"] = str(is_bold)
        section["TempFontItalic"] = str(is_italic)

        (pos_x, pos_y) = self._pos_co2.get_result()
        section["CO2Pos"] = "({0},{1})".format(pos_x, pos_y)
        (pos_x, pos_y) = self._pos_temp.get_result()
        section["TempPos"] = "({0},{1})".format(pos_x, pos_y)

    def _select_warn_color(self) -> None:
        (triple_color, tk_color) = colorchooser.askcolor(self._warn_color)
        if triple_color is None:
            return
        self._warn_selector.configure(foreground=tk_color)
        self._warn_color = (int(triple_color[0]), int(triple_color[1]), int(triple_color[2]))

    def _select_crit_color(self) -> None:
        (triple_color, tk_color) = colorchooser.askcolor(self._crit_color)
        if triple_color is None:
            return
        self._crit_selector.configure(foreground=tk_color)
        self._crit_color = (int(triple_color[0]), int(triple_color[1]), int(triple_color[2]))

    def _get_tuple(self, value: str) -> Tuple[int, ...]:
        """  Конвертирует строку '0, 0' в кортеж (0, 0)
             Конвертирует строку '0, 0, 0' в кортеж (0, 0, 0) """
        return tuple(int(item.strip("([ '])")) for item in value.split(",") if item.strip())
