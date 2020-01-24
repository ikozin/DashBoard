from typing import Dict, Tuple
from configparser import ConfigParser
from tkinter import IntVar, StringVar, Entry, LabelFrame, Label, Spinbox, N, S, E, W, RIGHT
from tkinter.ttk import Frame
from ext.base_manager import BaseManager
from ext.modal_dialog import FontChooserFrame, XYFrame


class Bme280Manager(BaseManager):
    """description of class"""

    def __init__(self, root: LabelFrame):
        """ """
        super(Bme280Manager, self).__init__(root, text="Настройки BME280, Параметры: Температура={0}, Влажность={1}, Давление={2}")
        self._address_value = IntVar()
        self._temperature_text_value = StringVar()
        self._humidity_text_value = StringVar()
        self._pressure_text_value = StringVar()
        self._format_text_value = StringVar()

        content = LabelFrame(self, text="Основные настрйки")
        content.grid(row=0, column=0, padx=2, pady=2, sticky=(N, S, E, W))

        lbl = Label(content, justify=RIGHT, text="Адрес модуля")
        lbl.grid(row=0, column=0, padx=2, pady=2, sticky=(N, S, E))
        spin = Spinbox(content, from_=1, to=255, increment=1, width=5, textvariable=self._address_value)
        spin.grid(row=0, column=1, padx=2, pady=2, sticky=(N, S, W))
        lbl = Label(content, justify=RIGHT, text="Формат текста")
        lbl.grid(row=1, column=0, padx=2, pady=2, sticky=(N, S, E))
        entr = Entry(content, width=60, textvariable=self._format_text_value)
        entr.grid(row=1, column=1, padx=2, pady=2, sticky=(N, S, E, W))

        content = LabelFrame(self, text="Температура")
        content.grid(row=1, column=0, padx=2, pady=2, sticky=(N, S, E, W))

        lbl = Label(content, justify=RIGHT, text="Текст")
        lbl.grid(row=0, column=0, padx=2, pady=2, sticky=(N, S, E))
        entr = Entry(content, width=68, textvariable=self._temperature_text_value)
        entr.grid(row=0, column=1, padx=2, pady=2, sticky=(N, S, E, W))
        self._pos_temperature = XYFrame(content, "Расположение", "Расположение (X)", "Расположение (Y)")
        self._pos_temperature.grid(row=1, column=0, columnspan=2, padx=2, pady=2, sticky=(N, S, E, W))

        content = LabelFrame(self, text="Влажность")
        content.grid(row=2, column=0, padx=2, pady=2, sticky=(N, S, E, W))

        lbl = Label(content, justify=RIGHT, text="Текст")
        lbl.grid(row=0, column=0, padx=2, pady=2, sticky=(N, S, E))
        entr = Entry(content, width=68, textvariable=self._humidity_text_value)
        entr.grid(row=0, column=1, padx=2, pady=2, sticky=(N, S, E, W))
        self._pos_humidity = XYFrame(content, "Расположение", "Расположение (X)", "Расположение (Y)")
        self._pos_humidity.grid(row=1, column=0, columnspan=2, padx=2, pady=2, sticky=(N, S, E, W))

        content = LabelFrame(self, text="Давление")
        content.grid(row=3, column=0, padx=2, pady=2, sticky=(N, S, E, W))

        lbl = Label(content, justify=RIGHT, text="Текст")
        lbl.grid(row=0, column=0, padx=2, pady=2, sticky=(N, S, E))
        entr = Entry(content, width=68, textvariable=self._pressure_text_value)
        entr.grid(row=0, column=1, padx=2, pady=2, sticky=(N, S, E, W))
        self._pos_pressure = XYFrame(content, "Расположение", "Расположение (X)", "Расположение (Y)")
        self._pos_pressure.grid(row=1, column=0, columnspan=2, padx=2, pady=2, sticky=(N, S, E, W))

        self._font = FontChooserFrame(self, "Параметры шрифта")
        self._font.grid(row=4, column=0, padx=2, pady=2, sticky=(N, S, E, W))

    def load(self, config: ConfigParser, module_list: Dict[str, BaseManager]) -> None:
        if not isinstance(config, ConfigParser):
            raise TypeError("config")
        if not config.has_section("BME280Block"):
            config.add_section("BME280Block")
        section = config["BME280Block"]
        self._address_value.set(section.getint("Address", fallback=118))
        font_name = section.get("FontName", fallback="Helvetica")
        font_size = section.getint("FontSize", fallback=150)
        is_bold = section.getboolean("FontBold", fallback=True)
        is_italic = section.getboolean("FontItalic", fallback=False)
        self._font.load(font_name, font_size, is_bold, is_italic)
        self._temperature_text_value.set(section.get("TemperatureText", fallback=""))
        self._humidity_text_value.set(section.get("HumidityText", fallback=""))
        self._pressure_text_value.set(section.get("PressureText", fallback=""))
        (pos_x, pos_y) = self._get_tuple(section.get("TemperaturePos", fallback="(0, 0)"))
        self._pos_temperature.load(pos_x, pos_y)
        (pos_x, pos_y) = self._get_tuple(section.get("HumidityPos", fallback="(0, 0)"))
        self._pos_humidity.load(pos_x, pos_y)
        (pos_x, pos_y) = self._get_tuple(section.get("PressurePos", fallback="(0, 0)"))
        self._pos_pressure.load(pos_x, pos_y)
        self._format_text_value.set(section.get("FormatText", fallback=""))

    def save(self, config: ConfigParser) -> None:
        if not isinstance(config, ConfigParser):
            raise TypeError("config")
        if not config.has_section("BME280Block"):
            config.add_section("BME280Block")
        section = config["BME280Block"]
        section["Address"] = str(self._address_value.get())
        (font_name, font_size, is_bold, is_italic) = self._font.get_result()
        section["FontName"] = font_name
        section["FontSize"] = str(font_size)
        section["FontBold"] = str(is_bold)
        section["FontItalic"] = str(is_italic)
        section["TemperatureText"] = self._temperature_text_value.get()
        section["HumidityText"] = self._humidity_text_value.get()
        section["PressureText"] = self._pressure_text_value.get()
        (pos_x, pos_y) = self._pos_temperature.get_result()
        section["TemperaturePos"] = "({0},{1})".format(pos_x, pos_y)
        (pos_x, pos_y) = self._pos_humidity.get_result()
        section["HumidityPos"] = "({0},{1})".format(pos_x, pos_y)
        (pos_x, pos_y) = self._pos_pressure.get_result()
        section["PressurePos"] = "({0},{1})".format(pos_x, pos_y)
        section["FormatText"] = self._format_text_value.get()

    def _get_tuple(self, value: str) -> Tuple[int, ...]:
        """  Конвертирует строку '0, 0, 0' в кортеж (0, 0, 0) """
        return tuple(int(item.strip("([ '])")) for item in value.split(",") if item.strip())
