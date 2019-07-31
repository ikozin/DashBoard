from typing import List
from configparser import ConfigParser
from tkinter import StringVar, Entry, LabelFrame, Label, N, S, E, W
from tkinter.ttk import Combobox
from ext.modal_dialog import ColorsChooserFrame
from ext.alarm.alarm_setting import AlarmSetting


class AlarmSettingText(AlarmSetting):

    def __init__(self, root, section_name: str, mod_List: List[str]):
        super(AlarmSettingText, self).__init__(root, section_name, mod_List)
        self._type = 5
        self._text_value = StringVar(value="")
        self._color_frame = ColorsChooserFrame(self, "Цвет")
        self._color_frame.grid(row=2, column=0, columnspan=2, sticky=(N, S, E, W))
        frame = LabelFrame(self, text="Сообщение")
        frame.grid(row=3, column=0, columnspan=2, sticky=(N, S, E, W))
        lbl = Label(frame, text="Текст:")
        lbl.grid(row=0, column=0, pady=2, sticky=(N, S, E))
        entry = Entry(frame, textvariable=self._text_value)
        entry.grid(row=0, column=1, padx=2, pady=2, sticky=(N, S, E, W))

    def load(self, config: ConfigParser, section_name: str) -> None:
        super(AlarmSettingText, self).load(config, section_name)
        section = config[section_name]
        back_color = self._get_tuple(section.get("BackgroundColor", fallback="(0, 0, 0)"))
        fore_color = self._get_tuple(section.get("ForegroundColor", fallback="(255, 255, 255)"))
        self._color_frame.load(back_color, fore_color)
        self._text_value.set(section.get("Text", fallback=""))

    def save(self, config: ConfigParser, section_name: str) -> None:
        super(AlarmSettingText, self).save(config, section_name)
        section = config[section_name]
        (background_color, foreground_color) = self._color_frame.get_result()
        section["BackgroundColor"] = "(%d, %d, %d)" % background_color
        section["ForegroundColor"] = "(%d, %d, %d)" % foreground_color
        section["Text"] = self._text_value.get()

