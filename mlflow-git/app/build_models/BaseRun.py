import abc


class BaseRun(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def run(self):
        """Required Method"""
