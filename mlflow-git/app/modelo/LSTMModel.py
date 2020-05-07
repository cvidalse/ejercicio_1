from .ModeloPrediccion import ModeloPrediccion
import pandas as pd
import tensorflow as tf
import numpy as np
import os


class LSTMModel(ModeloPrediccion):

    def __init__(self):
        tf.enable_eager_execution()
        self.data = pd.read_csv(
            "https://raw.githubusercontent.com/FabianMariqueo/dataset-sinca/master/sinca_encinas_2015_2109.csv", parse_dates=['Fecha'], index_col='Fecha')

        self.__multi_step_model = None
        self.__path_model = "models_file"

        if not os.path.exists(os.getcwd()+"/"+self.__path_model):
            self.modelo_prediccion(self.data)
        else:
            print("Model is already loaded")

    # TensorFlow tiene su propio metodo para generar un archivo y guardar el modelo entrenado
    def get_model(self):
        if not os.path.exists(os.getcwd()+"/"+self.__path_model):
            tf.keras.experimental.export_saved_model(
                self.__multi_step_model, self.__path_model)
        return os.getcwd()+"/"+self.__path_model

    def modelo_prediccion(self, data):
        # obtener solo los valores del dataset
        dataset = data.values
        future_target = 24
        TRAIN_SPLIT = 26280
        past_history = 72
        STEP = 1
        x_train_multi, y_train_multi = self.__multivariate_data(dataset, dataset[:, 0], 0,
                                                                TRAIN_SPLIT, past_history,
                                                                future_target, STEP)
        x_val_multi, y_val_multi = self.__multivariate_data(dataset, dataset[:, 0],
                                                            TRAIN_SPLIT, None, past_history,
                                                            future_target, STEP)

        BATCH_SIZE = 256
        BUFFER_SIZE = 10000
        # se crean los tensores basados en dataframe
        train_data_multi = tf.data.Dataset.from_tensor_slices(
            (x_train_multi, y_train_multi))
        train_data_multi = train_data_multi.cache().shuffle(
            BUFFER_SIZE).batch(BATCH_SIZE).repeat()

        val_data_multi = tf.data.Dataset.from_tensor_slices(
            (x_val_multi, y_val_multi))
        val_data_multi = val_data_multi.batch(BATCH_SIZE).repeat()

        # crea el modelo en keras
        self.__multi_step_model = tf.keras.models.Sequential()
        self.__multi_step_model.add(tf.keras.layers.LSTM(32,
                                                         return_sequences=True,
                                                         input_shape=x_train_multi.shape[-2:]))
        self.__multi_step_model.add(
            tf.keras.layers.LSTM(16, activation='relu'))
        # la densidad debe coincidir con el numero de horas que se busca predecir
        self.__multi_step_model.add(tf.keras.layers.Dense(24))

        self.__multi_step_model.compile(optimizer=tf.keras.optimizers.RMSprop(
            clipvalue=1.0), loss='mae', metrics=['mae', 'mse'])

        # se entrena el modelo con los tensores creados anteriormente
        EVALUATION_INTERVAL = 200
        EPOCHS = 5
        multi_step_history = self.__multi_step_model.fit(train_data_multi, epochs=EPOCHS,
                                                         steps_per_epoch=EVALUATION_INTERVAL,
                                                         validation_data=val_data_multi,
                                                         validation_steps=50, use_multiprocessing=False)

    # método mediante el cual se obtienen los datos utilizados para las predicciones y para entrenar
    # dataset equivale a los datos en total
    # target son los datos que se buscan predecir
    # start_index y end_index define que datos del dataframe se cuentan
    # history_size es la cantidad de datos anteriores que se tomaran
    # target size define la cantidad de horas a predecir

    def __multivariate_data(self, dataset, target, start_index, end_index, history_size,
                            target_size, step, single_step=False):
        data = []
        labels = []

        start_index = start_index + history_size
        if end_index is None:
            end_index = len(dataset) - target_size

        for i in range(start_index, end_index):
            indices = range(i-history_size, i, step)
            data.append(dataset[indices])

            if single_step:
                labels.append(target[i+target_size])
            else:
                labels.append(target[i:i+target_size])

        return np.array(data), np.array(labels)
