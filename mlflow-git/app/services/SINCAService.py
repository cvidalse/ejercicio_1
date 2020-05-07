import requests
import json
import datetime
import pandas as pd
import numpy as np
from datetime import datetime


class SINCAService(object):

    __url = "https://sinca.mma.gob.cl/cgi-bin/APUB-MMA/apub.tsindico2.cgi"

    __querystring = {
        "outtype": "xcl",
        "macro": "",
        "from": "",
        "to": "",
        "path": "/usr/airviro/data/CONAMA/",
        "lang": "esp",
        "rsrc": "",
        "macropath": ""
    }

    def contaminacion(self, startDate, endDate, param_contaminacion):
        self.__querystring["from"] = startDate
        self.__querystring["to"] = endDate
        self.__querystring["macro"] = param_contaminacion

        response = requests.request(
            "GET", self.__url, params=self.__querystring, verify=False)

        data_response = response.text.split("\n")
        # En el primer registro se encuentran las cabezeras del dataset
        data_response[0] += "Registros validados;Registros preliminares;Registros no validados;"
        data_array = []
        for row in data_response:
            if len(row) < 1:
                break
            # Almacenar los registros en un array para poder transformarlos en pandasdataframe
            registro = row.split(";")
            if "FECHA (YYMMDD)" not in registro[0]:
                registro[0] = self.__date_converter(registro[0], registro[1])
            data_array.append(registro)
        data_array = np.array(data_array)
        dataframe = pd.DataFrame(
            data=data_array[1:, 0:], columns=data_array[0, 0:])
        dataframe = dataframe.rename(
            columns={"FECHA (YYMMDD)": "Fecha", "Registros preliminares": "PM25"})
        dataframe = dataframe.drop(
            ['HORA (HHMM)', 'Registros validados', 'Registros no validados', ''], axis=1)
        dataframe['PM25'] = pd.to_numeric(dataframe['PM25'], errors='coerce')
        dataframe = dataframe.dropna()
        return dataframe

    # Fecha (YYMMDD), Hora(HHMM); Retorna objeto datetime

    def __date_converter(self, fecha, hora):
        day = int(fecha[-2:])
        month = int(fecha[-4:-2])
        year = 2000 + int(fecha[:-4])

        hours = int(hora[:2])
        minutes = int(hora[2:])

        return datetime(year, month, day, hours, minutes)
