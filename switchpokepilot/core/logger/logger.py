from abc import ABCMeta, abstractmethod


class Logger(metaclass=ABCMeta):
    @abstractmethod
    def debug(self, message):
        raise NotImplementedError

    @abstractmethod
    def info(self, message):
        raise NotImplementedError

    @abstractmethod
    def warn(self, message):
        raise NotImplementedError

    @abstractmethod
    def error(self, message):
        raise NotImplementedError
