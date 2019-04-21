from typing import *

from ext.AlarmSettingTimeFile import AlarmSettingTimeFile


class AlarmSettingRise(AlarmSettingTimeFile):
    def __init__(self, root, sectionName: str):
        """ """
        super(AlarmSettingRise, self).__init__(root, sectionName)
        self._type = 3

