from typing import List
from configparser import ConfigParser
from tkinter import IntVar, LabelFrame, Label, Spinbox, N, S, E, W
from ext.modal_dialog import ColorsChooserFrame
from ext.alarm.alarm_setting import AlarmSetting


class AlarmSettingUI(AlarmSetting):
    """description of class"""

    def __init__(self, root: LabelFrame, section_name: str, mod_list: List[str]):
        super(AlarmSettingUI, self).__init__(root, section_name, mod_list)
        self._duration_variable = IntVar(value=0)
        duration_frame = LabelFrame(self, text="Длительность")
        duration_frame.grid(row=1, column=1, sticky=(N, S, E, W))
        spin = Spinbox(duration_frame, from_=5, to=60, increment=1, width=3, textvariable=self._duration_variable)
        spin.grid(row=0, column=0, padx=2, pady=2)
        lbl = Label(duration_frame, text="секунд")
        lbl.grid(row=0, column=1, pady=2)
        self._color_frame = ColorsChooserFrame(self, "Цвет")
        self._color_frame.grid(row=2, column=0, columnspan=2, sticky=(N, S, E, W))

    def load(self, config: ConfigParser, section_name: str) -> None:
        super(AlarmSettingUI, self).load(config, section_name)
        section = config[section_name]
        duration = section.getint("Duration", fallback=5)
        self._duration_variable.set(duration)
        back_color = self._get_tuple(section.get("BackgroundColor", fallback="(0, 0, 0)"))
        fore_color = self._get_tuple(section.get("ForegroundColor", fallback="(255, 255, 255)"))
        self._color_frame.load(back_color, fore_color)

    def save(self, config: ConfigParser, section_name: str) -> None:
        super(AlarmSettingUI, self).save(config, section_name)
        section = config[section_name]
        (background_color, foreground_color) = self._color_frame.get_result()
        section["Duration"] = str(self._duration_variable.get())
        section["BackgroundColor"] = "(%d, %d, %d)" % background_color
        section["ForegroundColor"] = "(%d, %d, %d)" % foreground_color
