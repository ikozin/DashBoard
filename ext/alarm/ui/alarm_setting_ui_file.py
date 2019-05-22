from typing import List
from configparser import ConfigParser
from tkinter import filedialog, StringVar, LabelFrame, Label, Entry, Button, N, S, E, W
from ext.alarm.ui.alarm_setting_ui import AlarmSettingUI


class AlarmSettingUIFile(AlarmSettingUI):

    def __init__(self, root, section_name: str, modList: List[str]):
        super(AlarmSettingUIFile, self).__init__(root, section_name, modList)
        self._file_variable = StringVar(value="")
        file_frame = LabelFrame(self, text="Файл для проигрывания")
        file_frame.grid(row=3, column=0, columnspan=2, sticky=(N, S, E, W))
        lbl = Label(file_frame, text="Файл:")
        lbl.grid(row=0, column=0, pady=2)
        entr = Entry(file_frame, width=34, textvariable=self._file_variable)
        entr.grid(row=0, column=1, pady=2)
        btn = Button(file_frame, text="...", command=self._select_file, width=3)
        btn.grid(row=0, column=2, pady=2)

    def load(self, config: ConfigParser, section_name: str) -> None:
        super(AlarmSettingUIFile, self).load(config, section_name)
        section = config[section_name]
        self._file_variable.set(section.get("File", fallback=""))

    def save(self, config: ConfigParser, section_name: str) -> None:
        super(AlarmSettingUIFile, self).save(config, section_name)
        section = config[section_name]
        section["File"] = self._file_variable.get()

    def _select_file(self) -> None:
        filename = filedialog.Open(self, filetypes=[('*.* all files', '.*')]).show()
        if filename == '':
            return
        self._file_variable.set(filename)
