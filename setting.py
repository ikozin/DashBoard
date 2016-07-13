import configparser 
import time

TEXT_EXCEPTION_NOT_FOUND = "Ошибка конфигурации! В секции [{0}] пропущен параметр {1}"
TEXT_EXCEPTION_FORMAT = "Ошибка конфигурации! В секции [{0}] не верный формат параметра {1}"

class Setting:

    def __init__(self):
        """Ininitializes a new instanse"""
        self.TimeBackgroudColor = None
        self.TimeForegroudColor = None
        self.IdleTime           = None
        self.TimeLine           = []         #Набор кортежей (StartTime, TimeBackgroudColor, TimeForegroudColor, IdleTime)
    
    def load(self, fileName):
        # Загружаем настройки
        config = configparser.ConfigParser()
        config.read(fileName, encoding="utf-8")

        section = config["DEFAULT"]
        self.TimeBackgroudColor = self._getTuple(section.get("BackgroudColor"))
        self.TimeForegroudColor = self._getTuple(section.get("ForegroudColor"))
        self.IdleTime           = section.getint("IdleTime")

        if not self.TimeBackgroudColor: raise Exception(TEXT_EXCEPTION_NOT_FOUND.format("DEFAULT", "BackgroudColor"))
        if not self.TimeForegroudColor: raise Exception(TEXT_EXCEPTION_NOT_FOUND.format("DEFAULT", "ForegroudColor"))
        if not self.IdleTime:           raise Exception(TEXT_EXCEPTION_NOT_FOUND.format("DEFAULT", "IdleTime"))

        if len(self.TimeBackgroudColor) != 3: raise Exception(TEXT_EXCEPTION_FORMAT.format("DEFAULT", "BackgroudColor"))
        if len(self.TimeForegroudColor) != 3: raise Exception(TEXT_EXCEPTION_FORMAT.format("DEFAULT", "ForegroudColor"))

        section = config["TIMELINE"]
        schemas = section.get("sections")
        if schemas:
            schemas = [item.strip(" '") for item in schemas.split(",") if item.strip()]
            for schema in schemas:
                if not config.has_section(schema):
                    raise Exception("Ошибка конфигурации! Нет секции [{0}]".format(schema))
                section = config[schema]
                start = section.get("StartTime")
                if not start:
                    raise Exception(TEXT_EXCEPTION_NOT_FOUND.format(schema, "StartTime"))
                start = time.strptime(start, "%H:%M:%S")
                backgroudColor = self._getTuple(section.get("BackgroudColor"))
                foregroudColor = self._getTuple(section.get("ForegroudColor"))
                idleTime       = section.getint('IdleTime', self.IdleTime)
                if not backgroudColor: backgroudColor = self.TimeBackgroudColor
                if not foregroudColor: foregroudColor = self.TimeForegroudColor
                if len(backgroudColor) != 3: raise Exception(TEXT_EXCEPTION_FORMAT.format(schema, "BackgroudColor"))
                if len(foregroudColor) != 3: raise Exception(TEXT_EXCEPTION_FORMAT.format(schema, "ForegroudColor"))
                entry = (start, backgroudColor, foregroudColor, idleTime)
                self.TimeLine.append(entry)
        if len(self.TimeLine) == 0:
            entry = (time.strptime("00:00:00", "%H:%M:%S"), self.TimeBackgroudColor, self.TimeForegroudColor, self.IdleTime)
            self.TimeLine.append(entry)
        list.sort(self.TimeLine, key=lambda entry: entry[0])


    def get_curret_setting(self):
        value = time.localtime()
        current = self.TimeLine[0]
        for line in self.TimeLine[1:]:
            if (value.tm_hour < line[0].tm_hour): break
            if (value.tm_min < line[0].tm_min): break
            if (value.tm_sec < line[0].tm_sec): break
            current = line
        return current


    def _getTuple(self, value):
        """  Конвертирует строку '0, 0, 0' в кортеж (0, 0, 0) """
        try:
            return tuple(int(item.strip("([ '])")) for item in value.split(",") if item.strip())
        except:
            return None

