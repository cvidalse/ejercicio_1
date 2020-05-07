from .BaseRun import BaseRun
from modelo.LSTMModel import LSTMModel
from conf.Configuration_manager import Configuration_manager
import tensorflow as tf


class TensorFlowRun(BaseRun):

    def __init__(self):
        # Archivo de configuración donde se guarda el modelo y la ruta del archivo pkl del modelo
        self.__config = Configuration_manager.load_config()

        self.__modelo = LSTMModel()

    def run(self):
        path_model = self.__modelo.get_model()
        print(path_model)
        # Guardar la ruta del modelo pkl en el archivo de configuracion
        self.__config['ruta_modelo_pkl'] = path_model
        Configuration_manager.save_values(self.__config)
