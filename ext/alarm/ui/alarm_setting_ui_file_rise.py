from typing import List
from ext.alarm.ui.alarm_setting_ui_file import AlarmSettingUIFile


class AlarmSettingUIRise(AlarmSettingUIFile):
    def __init__(self, root, section_name: str, mod_list: List[str]):
        """ """
        super(AlarmSettingUIRise, self).__init__(root, section_name, mod_list)
        self._type = 3
