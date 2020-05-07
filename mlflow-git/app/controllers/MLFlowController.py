from .Controller import Controller
from services.Meteored_service import MeteoredService
from conf.Configuration_manager import Configuration_manager
import pickle
import json
import datetime
import os


class MLFlowController(Controller):

    def __init__(self):
        self.__conf = Configuration_manager.load_config()
        self.__meteoredService = MeteoredService()
        # Cargar el modelo pkl desde el archivo de configuracion que se encuentra dentro de la carpeta del modelo
        path_model = self.__conf["ruta_modelo_pkl"] + "/model.pkl"
        self.__loaded_model = pickle.load(open(path_model, 'rb'))

    def run(self):
        # Obtener prediccion de los datos meteorologicos
        meteored_data = self.__meteoredService.get_data

        # Predecir los datos con los datos meteorológicos obtenidos
        prediccion = self.__loaded_model.predict(meteored_data['data'])

        # La fecha de expiracion de los datos es en una hora mas
        fecha_expiracion = datetime.datetime.now() + datetime.timedelta(hours=1)
        json_prediccion = {
            "fecha_expiracion": str(fecha_expiracion),
            "data": []
        }
        # Si la longitud de ambos arrays coincide
        if len(prediccion) == len(meteored_data["horas"]):
            print("No problem!!")
            # Ordenar los datos para generar el archivo
            for i in range(len(prediccion)):
                json_prediccion["data"].append({
                    "fecha": meteored_data["horas"][i],
                    "categoria": self.__categoria(prediccion[i])
                })

            file_dir = os.path.dirname(os.path.abspath(__file__))
            file_route = '/prediccion.json'
            file_option = 'w'
            with open(file_dir + file_route, file_option) as outfile:
                json.dump(json_prediccion, outfile)

    # Categorías para los rangos de PM 2.5
    def __categoria(self, pm25):
        if pm25 <= 79:
            return "Bueno"
        elif pm25 >= 80 and pm25 <= 169:
            return "Poco Saludable"
        else:
            return "Peligroso"
