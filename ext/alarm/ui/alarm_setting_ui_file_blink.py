from typing import List
from ext.alarm.ui.alarm_setting_ui_file import AlarmSettingUIFile


class AlarmSettingUIBlink(AlarmSettingUIFile):

    def __init__(self, root, section_name: str, mod_list: List[str]):
        super(AlarmSettingUIBlink, self).__init__(root, section_name, mod_list)
        self._type = 2
