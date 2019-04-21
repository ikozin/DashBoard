from typing import *

from ext.AlarmSettingTimeFile import AlarmSettingTimeFile


class AlarmSettingBlink(AlarmSettingTimeFile):
    def __init__(self, root, sectionName: str):
        """ """
        super(AlarmSettingBlink, self).__init__(root, sectionName)
        self._type = 2

