import sys

from exceptions import ExceptionNotFound
from modules.BlockBase import BlockBase
from logging import Logger
from setting import Setting

CONFIG_FILE_NAME = "IR.ini"
PROG_NAME = "dashboard"


class BlockIR(BlockBase):
    """description of class"""

    def __init__(self, logger: Logger, setting: Setting):
        """Initializes (declare internal variables)"""
        super(BlockIR, self).__init__(logger, setting)
        self._module_list = None
        self._list = None

    def init(self, mod_list) -> None:
        """Initializes (initialize internal variables)"""
        # Загружаем настройки
        section = self._setting.configuration["IRBlock"]
        self._list = dict()
        self._module_list = mod_list
        for key_code in section:
            self._list[key_code.upper()] = section.get(key_code)
            module_name = self._list[key_code.upper()].split(",")[0]
            if module_name not in self._module_list:
                raise ExceptionNotFound(section.name, key_code.upper())
        with open(CONFIG_FILE_NAME, "w", encoding="utf-8") as file:
            for key_code in self._list:
                file.write("begin\n\tprog={1}\n\tbutton={0}\n\t"
                           "config={0}\n\trepeat=0\nend\n".format(key_code, PROG_NAME))
        self.module_init()
        # self.update_info(True)

    def procced_event(self, event, is_online):
        self.execute()

    def execute(self, *args) -> None:
        try:
            code = args[0] if len(args) == 1 else self.module_getcode()
            if not code:
                return
            key_code = code[0]
            if key_code not in self._list:
                return
            values = self._list[key_code].split(",")
            if values[0] in self._module_list:
                if len(values) == 2:
                    self._module_list[values[0]].execute(values[1])
                else:
                    self._module_list[values[0]].execute()

        except Exception as ex:
            self._logger.exception(ex)

    def done(self) -> None:
        self.module_done()


###########################################################################
    if sys.platform == "linux":  # Only for Raspberry Pi
        # import lirc

        def module_init(self):
            # lirc.init(PROG_NAME, CONFIG_FILE_NAME, blocking=False)
            pass

        def module_done(self):
            # lirc.deinit()
            pass

        def module_getcode(self, code=None):
            # code = lirc.nextcode()
            # return code
            return None

    else:
        def module_init(self):
            pass

        def module_done(self):
            pass

        def module_getcode(self, code=None):
            return code
###########################################################################
