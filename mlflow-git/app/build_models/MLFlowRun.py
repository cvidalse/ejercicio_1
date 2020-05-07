from .BaseRun import BaseRun
import mlflow
import importlib
from conf.Configuration_manager import Configuration_manager


class MLFlowRun(BaseRun):

    def __init__(self):
        # Archivo de configuración donde se guarda el modelo y la ruta del archivo pkl del modelo
        self.__config = Configuration_manager.load_config()

        # Modelo cargado desde un archivo de configuración
        ModeloPrediccion = getattr(importlib.import_module(
            "modelo." + self.__config['modelo']),  self.__config['modelo'])
        self.__mlflow_api = importlib.import_module(
            self.__config["mlflow_api"])

        self.modelo = ModeloPrediccion()

    def run(self):
        with mlflow.start_run():

            # Guardar el modelo pkl
            self.__mlflow_api.log_model(self.modelo.get_model(), 'model')

            # Obtener la ruta del pkl donde quedo guardado
            artifact_path = mlflow.get_artifact_uri()
            artifact_path = artifact_path.replace("file://", "")
            print(artifact_path)

            # Guardar la ruta del modelo pkl en el archivo de configuracion
            self.__config['ruta_modelo_pkl'] = artifact_path + "/model"
            Configuration_manager.save_values(self.__config)
