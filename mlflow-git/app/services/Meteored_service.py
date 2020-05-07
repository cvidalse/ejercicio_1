import requests
import json
import datetime

class MeteoredService(object):

    url = "https://api.meteored.cl/index.php"

    querystring = {
            "api_lang":"cl",
            "localidad":"18267",
            "affiliate_id":"zqiwenyt8418",
            "v":"3.0"
        }

    headers = {}    
    
    def get_data(self):
        response = requests.request("GET", self.url, headers=self.headers, params=self.querystring)

        response_json = json.loads(response.text)        

        ## Array con las predicciones de los 5 días futuros
        dias = response_json['day']

        ## Fecha del primer día    
        date = dias['1']['date']
        year = int(date[:4])
        month = int(date[4:6])
        day = int(date[6:])

        hour = dias['1']['hour'][0]['interval']
        hour = int(hour[:2])
        startDate = datetime.datetime(year,month,day,hour)

        ## Data para hacer la predicción (array de datos meteorológicos)
        data = []
        hora_data = []

        for key_dia in dias:
            horas = dias[key_dia]['hour']
            for hora in horas:
                
                if startDate > datetime.datetime.now():
                    hora_data.append(str(startDate))
                    dataHour = []
                    dataHour.append(hora['rain'])
                    dataHour.append(hora['humidity'])
                    dataHour.append(self.__direccionViento(hora['wind']['dir']))
                    dataHour.append(hora['temp'])
                    data.append(dataHour)
                ## Las predicciones vienen cada 3 horas
                startDate = startDate + datetime.timedelta(hours=3)
        return {
            "data":data,
            "horas":hora_data
        }
        

    def __direccionViento(self, dirViento):
        
        direccion = {
            "N":0,
            "NE":45,
            "E":90,
            "SE":135,
            "S":180,
            "SW":225,
            "W":270,
            "NW":315
        }        

        return direccion[dirViento]