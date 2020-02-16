from typing import Dict
from configparser import ConfigParser
from tkinter import IntVar, StringVar, LabelFrame, Label, Entry, Spinbox, N, S, E, W, RIGHT
from tkinter.ttk import Frame
from ext.base_manager import BaseManager
from ext.modal_dialog import FontChooserFrame


class YandexNewsManager(BaseManager):
    """description of class"""

    def __init__(self, root: LabelFrame):
        """ """
        super(YandexNewsManager, self).__init__(root, text="Настройки новостей от Яндекса")

        self._url_value = StringVar()
        self._update_value = IntVar()
        self._pos_value = IntVar()
        self._indent_value = IntVar()
        self._rows_value = IntVar()
        self._format_text_value = StringVar()

        content1 = Frame(self)
        content1.grid(row=0, column=0, columnspan=2, padx=2, pady=2, sticky=(N, S, E, W))

        lbl = Label(content1, text="Адрес")
        lbl.grid(row=0, column=0, padx=2, pady=2)

        entr = Entry(content1, textvariable=self._url_value, width=32)
        entr.grid(row=0, column=1, padx=2, pady=2)

        lbl = Label(content1, text="Время обновления")
        lbl.grid(row=0, column=2, padx=2, pady=2)

        spin = Spinbox(content1, from_=5, to=60, increment=1, width=3, textvariable=self._update_value)
        spin.grid(row=0, column=3, padx=2, pady=2)

        lbl = Label(content1, text="минут")
        lbl.grid(row=0, column=4, padx=2, pady=2)

        content2 = Frame(self)
        content2.grid(row=1, column=0, columnspan=2, padx=2, pady=2, sticky=(N, S, E, W))

        lbl = Label(content2, text="Распложение (Y)")
        lbl.grid(row=0, column=0, padx=2, pady=2)

        spin = Spinbox(content2, from_=1, to=1000, increment=1, width=5, textvariable=self._pos_value)
        spin.grid(row=0, column=1, padx=2, pady=2)

        lbl = Label(content2, text="Отступ по верикали")
        lbl.grid(row=0, column=2, padx=2, pady=2)

        spin = Spinbox(content2, from_=1, to=300, increment=1, width=3, textvariable=self._indent_value)
        spin.grid(row=0, column=3, padx=2, pady=2)

        lbl = Label(content2, text="Кол-во новостей")
        lbl.grid(row=0, column=4, padx=2, pady=2)

        spin = Spinbox(content2, from_=1, to=10, increment=1, width=3, textvariable=self._rows_value)
        spin.grid(row=0, column=5, padx=2, pady=2)

        self._font = FontChooserFrame(self, "Параметры шрифта")
        self._font.grid(row=2, column=0, columnspan=2, padx=2, pady=2, sticky=(N, S, E, W))

        lbl = Label(self, justify=RIGHT, text="Формат текста")
        lbl.grid(row=3, column=0, padx=2, pady=2, sticky=(N, S, E))

        entr = Entry(self, width=60, textvariable=self._format_text_value)
        entr.grid(row=3, column=1, padx=2, pady=2, sticky=(N, S, E, W))

    def load(self, config: ConfigParser, module_list: Dict[str, BaseManager]) -> None:
        if not isinstance(config, ConfigParser):
            raise TypeError("config")
        if not config.has_section("YandexNewsBlock"):
            config.add_section("YandexNewsBlock")
        section = config["YandexNewsBlock"]
        font_name = section.get("FontName", fallback="Helvetica")
        font_size = section.getint("FontSize", fallback=34)
        is_bold = section.getboolean("FontBold", fallback=False)
        is_italic = section.getboolean("FontItalic", fallback=False)
        self._font.load(font_name, font_size, is_bold, is_italic)
        self._url_value.set(section.get("Url", fallback="https://news.yandex.ru/index.rss"))
        self._update_value.set(section.getint("UpdateTime", fallback=15))
        self._pos_value.set(section.getint("Position", fallback=720))
        self._indent_value.set(section.getint("Indent", fallback=16))
        self._rows_value.set(section.getint("Rows", fallback=5))
        self._format_text_value.set(section.get("FormatText", fallback=""))

    def save(self, config: ConfigParser) -> None:
        if not isinstance(config, ConfigParser):
            raise TypeError("config")
        if not config.has_section("YandexNewsBlock"):
            config.add_section("YandexNewsBlock")
        section = config["YandexNewsBlock"]
        (font_name, font_size, is_bold, is_italic) = self._font.get_result()
        section["FontName"] = font_name
        section["FontSize"] = str(font_size)
        section["FontBold"] = str(is_bold)
        section["FontItalic"] = str(is_italic)
        section["Url"] = self._url_value.get()
        section["UpdateTime"] = str(self._update_value.get())
        section["Position"] = str(self._pos_value.get())
        section["Indent"] = str(self._indent_value.get())
        section["Rows"] = str(self._rows_value.get())
        section["FormatText"] = self._format_text_value.get()
