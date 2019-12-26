from abc import ABCMeta, abstractmethod


class HalGpio(metaclass=ABCMeta):
    """description of class"""
    def __init__(self):
        """Initializes (declare internal variables)"""
        pass

    def __del__(self):
        """Destructor"""
        pass

    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def done(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def display_off(self):
        pass

    @abstractmethod
    def display_on(self):
        pass

    @abstractmethod
    def reboot(self):
        pass

    @abstractmethod
    def shutdown(self):
        pass

    @abstractmethod
    def ledOn(self):
        pass

    @abstractmethod
    def ledOff(self):
        pass
