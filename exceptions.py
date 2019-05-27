class ExceptionFormat(Exception):
    """description of class"""

    def __init__(self, config_name, param_name):
        super(ExceptionFormat, self).__init__()
        self.config_name = config_name
        self.param_name = param_name

    def __str__(self):
        return "Ошибка конфигурации!" \
            " В секции [{0}] не верный формат параметра {1}".format(self.config_name, self.param_name)


class ExceptionNotFound(Exception):
    """description of class"""

    def __init__(self, config_name, param_name):
        super(ExceptionNotFound, self).__init__()
        self.config_name = config_name
        self.param_name = param_name

    def __str__(self):
        return "Ошибка конфигурации!" \
            " В секции [{0}] пропущен параметр {1}".format(self.config_name, self.param_name)
