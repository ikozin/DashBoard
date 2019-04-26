from typing import *

from ext.AlarmSettingTimeFile import AlarmSettingTimeFile


class AlarmSettingRise(AlarmSettingTimeFile):
    def __init__(self, root, sectionName: str, modList: List[str]):
        """ """
        super(AlarmSettingRise, self).__init__(root, sectionName, modList)
        self._type = 3

