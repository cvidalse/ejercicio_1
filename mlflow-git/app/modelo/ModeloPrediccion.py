import abc


class ModeloPrediccion(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def modelo_prediccion(self, data):
        """Required Method"""

    @abc.abstractmethod
    def get_model(self):
        """Required Method"""
