from typing import *

from ext.AlarmSettingTimeFile import AlarmSettingTimeFile


class AlarmSettingSimple(AlarmSettingTimeFile):
    def __init__(self, root, sectionName: str, modList: List[str]):
        """ """
        super(AlarmSettingSimple, self).__init__(root, sectionName, modList)
        self._type = 1

