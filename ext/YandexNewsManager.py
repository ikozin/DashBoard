from typing import *

from configparser import ConfigParser
from tkinter import *

from ext.BaseManager import BaseManager
from ext.ModalDialog import FontChooserFrame


class YandexNewsManager(BaseManager):
    """description of class"""

    def __init__(self, root: LabelFrame):
        """ """
        super(YandexNewsManager, self).__init__(root, text="Настройки новостей от Яндекса")

        self._urlValue = StringVar()
        self._updateValue = IntVar()
        self._posValue = IntVar()
        self._indentValue = IntVar()
        self._rowsValue = IntVar()

        content1 = ttk.Frame(self)
        content1.grid(row=0, column=0, padx=2, pady=2, sticky=(N, S, E, W))

        lbl = Label(content1, text="Адрес")
        lbl.grid(row=0, column=0, padx=2, pady=2)

        entr = Entry(content1, textvariable=self._urlValue, width=32)
        entr.grid(row=0, column=1, padx=2, pady=2)

        lbl = Label(content1, text="Время обновления")
        lbl.grid(row=0, column=2, padx=2, pady=2)

        spin = Spinbox(content1, from_=5, to=60, increment=1, width=3, textvariable=self._updateValue)
        spin.grid(row=0, column=3, padx=2, pady=2)

        lbl = Label(content1, text="минут")
        lbl.grid(row=0, column=4, padx=2, pady=2)

        content2 = ttk.Frame(self)
        content2.grid(row=1, column=0, padx=2, pady=2, sticky=(N, S, E, W))

        lbl = Label(content2, text="Распложение (Y)")
        lbl.grid(row=0, column=0, padx=2, pady=2)

        spin = Spinbox(content2, from_=1, to=1000, increment=1, width=5, textvariable=self._posValue)
        spin.grid(row=0, column=1, padx=2, pady=2)

        lbl = Label(content2, text="Отступ по верикали")
        lbl.grid(row=0, column=2, padx=2, pady=2)

        spin = Spinbox(content2, from_=1, to=300, increment=1, width=3, textvariable=self._indentValue)
        spin.grid(row=0, column=3, padx=2, pady=2)

        lbl = Label(content2, text="Кол-во новостей")
        lbl.grid(row=0, column=4, padx=2, pady=2)

        spin = Spinbox(content2, from_=1, to=10, increment=1, width=3, textvariable=self._rowsValue)
        spin.grid(row=0, column=5, padx=2, pady=2)

        self._font = FontChooserFrame(self, "Параметры шрифта")
        self._font.grid(row=2, column=0, padx=2, pady=2, sticky=(N, S, E, W))

    def load(self, config: ConfigParser, modulelist: Dict[str, BaseManager]) -> None:
        if not isinstance(config, ConfigParser):
            raise TypeError("config")
        if not config.has_section("YandexNewsBlock"):
            config.add_section("YandexNewsBlock")
        section = config["YandexNewsBlock"]
        fontName = section.get("FontName", "Helvetica")
        fontSize = section.getint("FontSize", 34)
        isBold = section.getboolean("FontBold", False)
        isItalic = section.getboolean("FontItalic", False)
        self._font.load(fontName, fontSize, isBold, isItalic)
        self._urlValue.set(section.get("Url", "https://news.yandex.ru/index.rss"))
        self._updateValue.set(section.getint("UpdateTime", 15))
        self._posValue.set(section.getint("Position", 720))
        self._indentValue.set(section.getint("Indent", 16))
        self._rowsValue.set(section.getint("Rows", 5))

    def save(self, config: ConfigParser) -> None:
        if not isinstance(config, ConfigParser):
            raise TypeError("config")
        if not config.has_section("YandexNewsBlock"):
            config.add_section("YandexNewsBlock")
        section = config["YandexNewsBlock"]
        (fontName, fontSize, isBold, isItalic) = self._font.getResult()
        section["FontName"] = fontName
        section["FontSize"] = str(fontSize)
        section["FontBold"] = str(isBold)
        section["FontItalic"] = str(isItalic)
        section["Url"] = self._urlValue.get()
        section["UpdateTime"] = str(self._updateValue.get())
        section["Position"] = str(self._posValue.get())
        section["Indent"] = str(self._indentValue.get())
        section["Rows"] = str(self._rowsValue.get())
