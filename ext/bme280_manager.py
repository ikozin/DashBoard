from typing import Dict, Tuple
from configparser import ConfigParser
from tkinter import IntVar, StringVar, Entry, LabelFrame, Label, Spinbox, N, S, E, W, RIGHT
from ext.base_manager import BaseManager
from ext.modal_dialog import DisplayTextFrame


class Bme280Manager(BaseManager):
    """description of class"""

    def __init__(self, root: LabelFrame):
        """ """
        super(Bme280Manager, self).__init__(root, text="Настройки BME280, Параметры: "
                                                       "Температура={0}, Влажность={1}, Давление={2}")
        self._address_value = IntVar()
        self._address_hex = StringVar()
        self._format_text_value = StringVar()

        content = LabelFrame(self, text="Основные настрйки")
        content.grid(row=0, column=0, padx=2, pady=2, sticky=(N, S, E, W))

        lbl = Label(content, justify=RIGHT, text="Адрес модуля")
        lbl.grid(row=0, column=0, padx=2, pady=2, sticky=(N, S, E))
        spin = Spinbox(content, from_=1, to=255, increment=1, width=5, textvariable=self._address_value)
        vcmd = (spin.register(self._address_to_hex), '%P')
        spin.configure(validate="key", validatecommand=vcmd)
        spin.grid(row=0, column=1, padx=2, pady=2, sticky=(N, S, W))
        lbl = Label(content, textvariable=self._address_hex)
        lbl.grid(row=0, column=2, padx=2, pady=2, sticky=(N, S, W))

        lbl = Label(content, justify=RIGHT, text="Формат текста")
        lbl.grid(row=1, column=0, padx=2, pady=2, sticky=(N, S, E))
        entr = Entry(content, width=60, textvariable=self._format_text_value)
        entr.grid(row=1, column=1, padx=2, pady=2, sticky=(N, S, E, W))

        self._temperature = DisplayTextFrame(self, "Температура", "Temperature")
        self._temperature.grid(row=1, column=0, padx=2, pady=2, sticky=(N, S, E, W))

        self._humidity = DisplayTextFrame(self, "Влажность", "Humidity")
        self._humidity.grid(row=2, column=0, padx=2, pady=2, sticky=(N, S, E, W))

        self._pressure = DisplayTextFrame(self, "Давление", "Pressure")
        self._pressure.grid(row=3, column=0, padx=2, pady=2, sticky=(N, S, E, W))

    def load(self, config: ConfigParser, module_list: Dict[str, BaseManager]) -> None:
        if not isinstance(config, ConfigParser):
            raise TypeError("config")
        if not config.has_section("BME280Block"):
            config.add_section("BME280Block")
        section = config["BME280Block"]
        self._address_value.set(section.getint("Address", fallback=118))
        self._format_text_value.set(section.get("FormatText", fallback=""))
        self._temperature.load(section)
        self._humidity.load(section)
        self._pressure.load(section)

    def save(self, config: ConfigParser) -> None:
        if not isinstance(config, ConfigParser):
            raise TypeError("config")
        if not config.has_section("BME280Block"):
            config.add_section("BME280Block")
        section = config["BME280Block"]
        section["Address"] = str(self._address_value.get())
        section["FormatText"] = self._format_text_value.get()
        self._temperature.save(section)
        self._humidity.save(section)
        self._pressure.save(section)

    def _address_to_hex(self, new: str) -> bool:
        try:
            self._address_hex.set("0x{:02X}".format(int(new)))
        except Exception:
            pass
        return True

    def _get_tuple(self, value: str) -> Tuple[int, ...]:
        """  Конвертирует строку '0, 0, 0' в кортеж (0, 0, 0) """
        return tuple(int(item.strip("([ '])")) for item in value.split(",") if item.strip())
