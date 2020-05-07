from .Controller import Controller
from conf.Configuration_manager import Configuration_manager
from services.SINCAService import SINCAService
from services import const_encinas
import tensorflow as tf
import numpy as np
from datetime import datetime, timedelta
import json
import os


class TensorFlowController(Controller):

    def __init__(self):
        self.__conf = Configuration_manager.load_config()
        self.__loaded_model = tf.keras.experimental.load_from_saved_model(
            self.__conf['ruta_modelo_pkl'])
        self.__sincaService = SINCAService()

    def run(self):
        endDate = datetime.utcnow() + timedelta(hours=-4)
        # La fecha de inicio es de 10 días anterior al día actual
        startDate = endDate + timedelta(days=-10)

        startDateStr = str(startDate.year - 2000) + \
            startDate.strftime('%m') + startDate.strftime('%d')
        endDateStr = str(endDate.year - 2000) + \
            endDate.strftime('%m') + endDate.strftime('%d')
        future_target = 24
        past_history = 72
        STEP = 1

        data = self.__sincaService.contaminacion(
            startDateStr, endDateStr, const_encinas.contaminacion["pm25"])
        data = data.set_index("Fecha")
        data = data.sort_index()
        # Los datos para la prediccion se limitan a el past_history + 1
        data = data[-(past_history+1):]
        dataset = data.values

        # Preparar datos para prediccion
        predict = self.__multivariate_data_predict(
            dataset, dataset[:], 0, None, past_history, future_target, STEP)

        prediction = self.__loaded_model.predict(predict)
        print("successful prediction")
        self.__save_prediction(prediction[0])
        print("saved successfully")

    def __save_prediction(self, prediction):
         # La fecha de expiracion de los datos es en una hora mas
        fecha_ahora = datetime.now() + timedelta(hours=-4)
        fecha_expiracion = fecha_ahora + timedelta(hours=1)

        json_prediccion = {
            "fecha_expiracion": str(fecha_expiracion),
            "data": []
        }

        print("No problem!!")
        # Ordenar los datos para generar el archivo
        for i in range(12):
            print(fecha_ahora+timedelta(hours=i))
            if (fecha_ahora+timedelta(hours=i)).hour==0:
                break
            json_prediccion["data"].append({
                "fecha": str(fecha_ahora + timedelta(hours=i)),
                "categoria": self.__categoria(prediction[i])
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

    # Metodo para preparar los datos para la prediccion
    def __multivariate_data_predict(self, dataset, target, start_index, end_index, history_size,
                                    target_size, step, single_step=False):
        data = []
        start_index = start_index + history_size
        if end_index is None:
            end_index = len(dataset)

        for i in range(start_index, end_index):
            indices = range(i-history_size, i, step)
            data.append(dataset[indices])
        return np.array(data)
