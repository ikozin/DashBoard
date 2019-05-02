from typing import *

from ext.alarm.ui.AlarmSettingUIFile import AlarmSettingUIFile


class AlarmSettingUI_Blink(AlarmSettingUIFile):
    def __init__(self, root, sectionName: str, modList: List[str]):
        """ """
        super(AlarmSettingUI_Blink, self).__init__(root, sectionName, modList)
        self._type = 2

