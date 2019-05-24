from typing import Dict, Tuple
from configparser import ConfigParser
from tkinter import IntVar, StringVar, LabelFrame, Label, Entry, Spinbox, N, S, E, W, RIGHT, LEFT
from tkinter.ttk import Frame
from ext.base_manager import BaseManager
from ext.modal_dialog import FontChooserFrame, XYFrame


class YandexWeatherManager(BaseManager):
    """description of class"""

    def __init__(self, root: LabelFrame):
        """ """
        super(YandexWeatherManager, self).__init__(root, text="Настройки YandexWeather")

        self._update_value = IntVar()
        self._region_id_value = IntVar()
        self._lat_value = StringVar()
        self._lon_value = StringVar()
        self._folder_value = StringVar()

        content = Frame(self)
        content.grid(row=0, column=0, padx=2, pady=2, sticky=(N, S, E, W))

        lbl = Label(content, justify=RIGHT, text="Время обновления")
        lbl.grid(row=0, column=0, padx=2, pady=2, sticky=(N, S, E))

        spin = Spinbox(content, from_=1, to=60, increment=1, width=5, textvariable=self._update_value)
        spin.grid(row=0, column=1, padx=2, pady=2, sticky=(N, S, E, W))

        lbl = Label(content, justify=LEFT, text="минут")
        lbl.grid(row=0, column=2, padx=2, pady=2, sticky=(N, S, W))

        lbl = Label(content, justify=RIGHT, text="Город")
        lbl.grid(row=1, column=0, padx=2, pady=2, sticky=(N, S, E))

        entr = Entry(content, width=40, textvariable=self._region_id_value)
        entr.grid(row=1, column=1, columnspan=2, padx=2, pady=2, sticky=(N, S, E, W))

        lbl = Label(content, justify=RIGHT, text="Широта (lat)")
        lbl.grid(row=2, column=0, padx=2, pady=2, sticky=(N, S, E))

        entr = Entry(content, width=40, textvariable=self._lat_value)
        entr.grid(row=2, column=1, columnspan=2, padx=2, pady=2, sticky=(N, S, E, W))

        lbl = Label(content, justify=RIGHT, text="Долгота (lon)")
        lbl.grid(row=3, column=0, padx=2, pady=2, sticky=(N, S, E))

        entr = Entry(content, width=40, textvariable=self._lon_value)
        entr.grid(row=3, column=1, columnspan=2, padx=2, pady=2, sticky=(N, S, E, W))

        lbl = Label(content, justify=RIGHT, text="Директория для картинок")
        lbl.grid(row=4, column=0, padx=2, pady=2, sticky=(N, S, E))

        entr = Entry(content, width=5, textvariable=self._folder_value)
        entr.grid(row=4, column=1, columnspan=2, padx=2, pady=2, sticky=(N, S, E, W))

        self._scale_icon = XYFrame(self, "Масштаб для картинки", "Масштаб (X)", "Масштаб (Y)")
        self._scale_icon.grid(row=1, column=0, padx=2, pady=2, sticky=(N, S, E, W))

        self._pos_icon = XYFrame(self, "Расположение для картинки", "Расположение (X)", "Расположение (Y)")
        self._pos_icon.grid(row=2, column=0, padx=2, pady=2, sticky=(N, S, E, W))

        self._pos_weather_type = XYFrame(self, "Расположение для погоды", "Расположение (X)", "Расположение (Y)")
        self._pos_weather_type.grid(row=3, column=0, padx=2, pady=2, sticky=(N, S, E, W))

        self._pos_temperature = XYFrame(self, "Расположение для температуры", "Расположение (X)", "Расположение (Y)")
        self._pos_temperature.grid(row=4, column=0, padx=2, pady=2, sticky=(N, S, E, W))

        self._pos_humidity = XYFrame(self, "Расположение для влажности", "Расположение (X)", "Расположение (Y)")
        self._pos_humidity.grid(row=5, column=0, padx=2, pady=2, sticky=(N, S, E, W))

        self._pos_pressure = XYFrame(self, "Расположение для давления", "Расположение (X)", "Расположение (Y)")
        self._pos_pressure.grid(row=6, column=0, padx=2, pady=2, sticky=(N, S, E, W))

        self._pos_wind = XYFrame(self, "Расположение для ветра", "Расположение (X)", "Расположение (Y)")
        self._pos_wind.grid(row=7, column=0, padx=2, pady=2, sticky=(N, S, E, W))

        self._weather_type = FontChooserFrame(self, "Параметры шрифта для погоды")
        self._weather_type.grid(row=8, column=0, padx=2, pady=2, sticky=(N, S, E, W))

        self._temperature = FontChooserFrame(self, "Параметры шрифта для температуры")
        self._temperature.grid(row=9, column=0, padx=2, pady=2, sticky=(N, S, E, W))

        self._humidity = FontChooserFrame(self, "Параметры шрифта для влажности")
        self._humidity.grid(row=10, column=0, padx=2, pady=2, sticky=(N, S, E, W))

        self._pressure = FontChooserFrame(self, "Параметры шрифта для давления")
        self._pressure.grid(row=11, column=0, padx=2, pady=2, sticky=(N, S, E, W))

        self._wind = FontChooserFrame(self, "Параметры шрифта ветра")
        self._wind.grid(row=12, column=0, padx=2, pady=2, sticky=(N, S, E, W))

    def load(self, config: ConfigParser, module_list: Dict[str, BaseManager]) -> None:
        if not isinstance(config, ConfigParser):
            raise TypeError("config")
        if not config.has_section("YandexWeatherBlock"):
            config.add_section("YandexWeatherBlock")
        section = config["YandexWeatherBlock"]

        self._update_value.set(section.getint("UpdateTime", fallback=15))
        self._region_id_value.set(section.getint("RegionId", fallback=213))
        self._lat_value.set(section.get("Lat", fallback=""))
        self._lon_value.set(section.get("Lon", fallback=""))
        self._folder_value.set(section.get("Folder", fallback=""))

        (pos_x, pos_y) = self._get_tuple(section.get("IconScale", fallback="(256, 256)"))
        self._scale_icon.load(pos_x, pos_y)
        (pos_x, pos_y) = self._get_tuple(section.get("IconPos", fallback="(0, 0)"))
        self._pos_icon.load(pos_x, pos_y)

        (pos_x, pos_y) = self._get_tuple(section.get("WeatherTypePos", fallback="(260, 242)"))
        self._pos_weather_type.load(pos_x, pos_y)
        (pos_x, pos_y) = self._get_tuple(section.get("TemperaturePos", fallback="(240, 50)"))
        self._pos_temperature.load(pos_x, pos_y)
        (pos_x, pos_y) = self._get_tuple(section.get("HumidityPos", fallback="(620, 98)"))
        self._pos_humidity.load(pos_x, pos_y)
        (pos_x, pos_y) = self._get_tuple(section.get("PressurePos", fallback="(620, 170)"))
        self._pos_pressure.load(pos_x, pos_y)
        (pos_x, pos_y) = self._get_tuple(section.get("WindPos", fallback="(620, 26)"))
        self._pos_wind.load(pos_x, pos_y)

        (font_name, font_size, is_bold, is_italic) = self.load_font(section, "WeatherTypeFont", is_bold_def=True)
        self._weather_type.load(font_name, font_size, is_bold, is_italic)

        (font_name, font_size, is_bold, is_italic) = self.load_font(section, "TemperatureFont",
                                                                    font_size_def=160, is_bold_def=True)
        self._temperature.load(font_name, font_size, is_bold, is_italic)

        (font_name, font_size, is_bold, is_italic) = self.load_font(section, "HumidityFont")
        self._humidity.load(font_name, font_size, is_bold, is_italic)

        (font_name, font_size, is_bold, is_italic) = self.load_font(section, "PressureFont")
        self._pressure.load(font_name, font_size, is_bold, is_italic)

        font_name = section.get("WindFontName", fallback="Helvetica")
        font_size = section.getint("WindFontSize", fallback=64)
        is_bold = section.getboolean("WindFontBold", fallback=False)
        is_italic = section.getboolean("WindFontItalic", fallback=False)
        self._wind.load(font_name, font_size, is_bold, is_italic)

    def save(self, config: ConfigParser) -> None:
        if not isinstance(config, ConfigParser):
            raise TypeError("config")
        if not config.has_section("YandexWeatherBlock"):
            config.add_section("YandexWeatherBlock")
        section = config["YandexWeatherBlock"]

        section["UpdateTime"] = str(self._update_value.get())
        section["RegionId"] = str(self._region_id_value.get())
        section["Lat"] = self._lat_value.get()
        section["Lon"] = self._lon_value.get()
        section["Folder"] = self._folder_value.get()

        (pos_x, pos_y) = self._scale_icon.get_result()
        section["IconScale"] = "({0},{1})".format(pos_x, pos_y)
        (pos_x, pos_y) = self._pos_icon.get_result()
        section["IconPos"] = "({0},{1})".format(pos_x, pos_y)

        (pos_x, pos_y) = self._pos_weather_type.get_result()
        section["WeatherTypePos"] = "({0},{1})".format(pos_x, pos_y)
        (pos_x, pos_y) = self._pos_temperature.get_result()
        section["TemperaturePos"] = "({0},{1})".format(pos_x, pos_y)
        (pos_x, pos_y) = self._pos_humidity.get_result()
        section["HumidityPos"] = "({0},{1})".format(pos_x, pos_y)
        (pos_x, pos_y) = self._pos_pressure.get_result()
        section["PressurePos"] = "({0},{1})".format(pos_x, pos_y)
        (pos_x, pos_y) = self._pos_wind.get_result()
        section["WindPos"] = "({0},{1})".format(pos_x, pos_y)

        (font_name, font_size, is_bold, is_italic) = self._weather_type.get_result()
        section["WeatherTypeFontName"] = font_name
        section["WeatherTypeFontSize"] = str(font_size)
        section["WeatherTypeFontBold"] = str(is_bold)
        section["WeatherTypeFontItalic"] = str(is_italic)

        (font_name, font_size, is_bold, is_italic) = self._temperature.get_result()
        section["TemperatureFontName"] = font_name
        section["TemperatureFontSize"] = str(font_size)
        section["TemperatureFontBold"] = str(is_bold)
        section["TemperatureFontItalic"] = str(is_italic)

        (font_name, font_size, is_bold, is_italic) = self._humidity.get_result()
        section["HumidityFontName"] = font_name
        section["HumidityFontSize"] = str(font_size)
        section["HumidityFontBold"] = str(is_bold)
        section["HumidityFontItalic"] = str(is_italic)

        (font_name, font_size, is_bold, is_italic) = self._pressure.get_result()
        section["PressureFontName"] = font_name
        section["PressureFontSize"] = str(font_size)
        section["PressureFontBold"] = str(is_bold)
        section["PressureFontItalic"] = str(is_italic)

        (font_name, font_size, is_bold, is_italic) = self._wind.get_result()
        section["WindFontName"] = font_name
        section["WindFontSize"] = str(font_size)
        section["WindFontBold"] = str(is_bold)
        section["WindFontItalic"] = str(is_italic)

    def _get_tuple(self, value: str) -> Tuple[int, ...]:
        """  Конвертирует строку '0, 0, 0' в кортеж (0, 0, 0) """
        return tuple(int(item.strip("([ '])")) for item in value.split(",") if item.strip())
