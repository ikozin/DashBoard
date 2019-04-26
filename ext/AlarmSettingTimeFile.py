from typing import *

from datetime import datetime
from configparser import ConfigParser
from tkinter import *
from tkinter import filedialog

from ext.BaseSetting import BaseSetting
from ext.ModalDialog import ColorsChooserFrame
from ext.AlarmSettingTime import AlarmSettingTime


class AlarmSettingTimeFile(AlarmSettingTime):
    def __init__(self, root, sectionName: str, modList: List[str]):
        """ """
        super(AlarmSettingTimeFile, self).__init__(root, sectionName, modList)
        self._fileVariable = StringVar(value="")

        fileFrame = LabelFrame(self, text="Файл для проигрывания")
        fileFrame.grid(row=3, column=0, columnspan=2, sticky=(N, S, E, W))

        lbl = Label(fileFrame, text="Файл:")
        lbl.grid(row=0, column=0, pady=2)

        entr = Entry(fileFrame, width=34, textvariable=self._fileVariable)
        entr.grid(row=0, column=1, pady=2)

        btn = Button(fileFrame, text="...", command=self._selectFile, width=3)
        btn.grid(row=0, column=2, pady=2)

    def load(self, config: ConfigParser, sectionName: str) -> None:
        """ """
        super(AlarmSettingTimeFile, self).load(config, sectionName)
        section = config[sectionName]
        self._fileVariable.set(section.get("File", ""))

    def save(self, config: ConfigParser, sectionName: str) -> None:
        """ """
        super(AlarmSettingTimeFile, self).save(config, sectionName)
        section = config[sectionName]
        section["File"] = self._fileVariable.get()

    def _selectFile(self) -> None:
        fileName = filedialog.Open(self, filetypes=[('*.* all files', '.*')]).show()
        if fileName == '':
            return
        self._fileVariable.set(fileName)

