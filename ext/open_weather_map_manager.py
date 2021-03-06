from configparser import ConfigParser
from tkinter import IntVar, StringVar, Label, Entry, Spinbox, N, S, E, W, RIGHT, LEFT
from tkinter.ttk import Frame
from ext.base_manager import BaseManager
from ext.modal_dialog import FontChooserFrame, XYFrame


class OpenWeatherMapManager(BaseManager):
    """description of class"""

    def __init__(self, root):
        """ """
        super(OpenWeatherMapManager, self).__init__(root, text="Настройки OpenWeatherMap")

        self._update_value = IntVar()
        self._key_value = StringVar()
        self._folder_value = StringVar()

        content = Frame(self)
        content.grid(row=0, column=0, padx=2, pady=2, sticky=(N, S, E, W))

        lbl = Label(content, justify=RIGHT, text="Время обновления")
        lbl.grid(row=0, column=0, padx=2, pady=2, sticky=(N, S, E))

        spin = Spinbox(content, from_=1, to=60, increment=1, width=5, textvariable=self._update_value)
        spin.grid(row=0, column=1, padx=2, pady=2, sticky=(N, S, E, W))

        lbl = Label(content, justify=LEFT, text="минут")
        lbl.grid(row=0, column=2, padx=2, pady=2, sticky=(N, S, W))

        lbl = Label(content, justify=RIGHT, text="Ключ")
        lbl.grid(row=1, column=0, padx=2, pady=2, sticky=(N, S, E))

        entr = Entry(content, width=40, textvariable=self._key_value)
        entr.grid(row=1, column=1, columnspan=2, padx=2, pady=2, sticky=(N, S, E, W))

        lbl = Label(content, justify=RIGHT, text="Директория для картинок")
        lbl.grid(row=2, column=0, padx=2, pady=2, sticky=(N, S, E))

        entr = Entry(content, width=5, textvariable=self._folder_value)
        entr.grid(row=2, column=1, columnspan=2, padx=2, pady=2, sticky=(N, S, E, W))

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

    def load(self, config, module_list):
        if not isinstance(config, ConfigParser):
            raise TypeError("config")
        if not config.has_section("OpenWeatherMapBlock"):
            config.add_section("OpenWeatherMapBlock")
        section = config["OpenWeatherMapBlock"]

        self._update_value.set(section.getint("UpdateTime", fallback=15))
        self._key_value.set(section.get("Key", fallback=""))
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

        font_name = section.get("WeatherTypeFontName", fallback="Helvetica")
        font_size = section.getint("WeatherTypeFontSize", fallback=64)
        is_bold = section.getboolean("WeatherTypeFontBold", fallback=True)
        is_italic = section.getboolean("WeatherTypeFontItalic", fallback=False)
        self._weather_type.load(font_name, font_size, is_bold, is_italic)

        font_name = section.get("TemperatureFontName", fallback="Helvetica")
        font_size = section.getint("TemperatureFontSize", fallback=160)
        is_bold = section.getboolean("TemperatureFontBold", fallback=True)
        is_italic = section.getboolean("TemperatureFontItalic", fallback=False)
        self._temperature.load(font_name, font_size, is_bold, is_italic)

        font_name = section.get("HumidityFontName", fallback="Helvetica")
        font_size = section.getint("HumidityFontSize", fallback=64)
        is_bold = section.getboolean("HumidityFontBold", fallback=False)
        is_italic = section.getboolean("HumidityFontItalic", fallback=False)
        self._humidity.load(font_name, font_size, is_bold, is_italic)

        font_name = section.get("PressureFontName", fallback="Helvetica")
        font_size = section.getint("PressureFontSize", fallback=64)
        is_bold = section.getboolean("PressureFontBold", fallback=False)
        is_italic = section.getboolean("PressureFontItalic", fallback=False)
        self._pressure.load(font_name, font_size, is_bold, is_italic)

        font_name = section.get("WindFontName", fallback="Helvetica")
        font_size = section.getint("WindFontSize", fallback=64)
        is_bold = section.getboolean("WindFontBold", fallback=False)
        is_italic = section.getboolean("WindFontItalic", fallback=False)
        self._wind.load(font_name, font_size, is_bold, is_italic)

    def save(self, config):
        if not isinstance(config, ConfigParser):
            raise TypeError("config")
        if not config.has_section("OpenWeatherMapBlock"):
            config.add_section("OpenWeatherMapBlock")
        section = config["OpenWeatherMapBlock"]

        section["UpdateTime"] = str(self._update_value.get())
        section["Key"] = self._key_value.get()
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

    def _get_tuple(self, value):
        """  Конвертирует строку '0, 0, 0' в кортеж (0, 0, 0) """
        return tuple(int(item.strip("([ '])")) for item in value.split(",") if item.strip())
