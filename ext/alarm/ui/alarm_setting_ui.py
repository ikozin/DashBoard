from typing import List
from configparser import ConfigParser
from tkinter import IntVar, LabelFrame, N, S, E, W
from ext.modal_dialog import ColorsChooserFrame
from ext.alarm.alarm_setting import AlarmSetting


class AlarmSettingUI(AlarmSetting):
    """description of class"""

    def __init__(self, root: LabelFrame, section_name: str, mod_list: List[str]):
        super(AlarmSettingUI, self).__init__(root, section_name, mod_list)
        self._color_frame = ColorsChooserFrame(self, "Цвет")
        self._color_frame.grid(row=2, column=0, columnspan=2, sticky=(N, S, E, W))

    def load(self, config: ConfigParser, section_name: str) -> None:
        super(AlarmSettingUI, self).load(config, section_name)
        section = config[section_name]
        back_color = self._get_tuple(section.get("BackgroundColor", fallback="(0, 0, 0)"))
        fore_color = self._get_tuple(section.get("ForegroundColor", fallback="(255, 255, 255)"))
        self._color_frame.load(back_color, fore_color)

    def save(self, config: ConfigParser, section_name: str) -> None:
        super(AlarmSettingUI, self).save(config, section_name)
        section = config[section_name]
        (background_color, foreground_color) = self._color_frame.get_result()
        section["BackgroundColor"] = "(%d, %d, %d)" % background_color
        section["ForegroundColor"] = "(%d, %d, %d)" % foreground_color
