import abc


class Controller(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def run(self):
        """Required Method"""

