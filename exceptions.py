class ExceptionFormat(Exception):
    """description of class"""

    def __init__(self, configName, paramName):
        super(ExceptionFormat, self).__init__()
        self.configName = configName
        self.paramName = paramName

    def __str__(self):
        return "Ошибка конфигурации!" \
            " В секции [{0}] не верный формат параметра {1}".format(self.configName, self.paramName)


class ExceptionNotFound(Exception):
    """description of class"""

    def __init__(self, configName, paramName):
        super(ExceptionNotFound, self).__init__()
        self.configName = configName
        self.paramName = paramName

    def __str__(self):
        return "Ошибка конфигурации!" \
            " В секции [{0}] пропущен параметр {1}".format(self.configName, self.paramName)
