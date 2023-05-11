import requests
from datetime import datetime
from dotenv import load_dotenv
import os
import numpy as np  
from datetime import datetime

load_dotenv()

class Connection():
    def __init__(self) -> None:
        self.__user_id = os.getenv('USER_ID')
        self.__format = os.getenv('FORMAT')
        self.__client_id = os.getenv('CLIENT_ID')
        self.__client_secret = os.getenv('CLIENT_SECRET')
        self.__logger = os.getenv('LOGGER')
        self.__parse_data = {}
        self.__data = {}
        self.__postData()

    @property
    def start_time(self) -> datetime:
        return datetime(datetime.now().year, datetime.now().month, datetime.now().day, 0, 0, 0).strftime("%Y-%m-%d %H:%M:%S")
    
    @property 
    def end_time(self) -> datetime:
        return datetime.today().strftime("%Y-%m-%d %H:%M:%S")

    @property
    def __parse_token(self):
        return {
            "url":"https://webservice.hobolink.com/ws/auth/token",
            "body":{
                "grant_type":"client_credentials",
                "client_id":self.__client_id,
                "client_secret":self.__client_secret
            },
            "headers":{
                'Accept':'application/json',
                'Content-Type':'application/x-www-form-urlencoded'
            }
        }
    
    # Build JSON
    @property
    def parse_data(self):
        return self.__parse_data
    
    @parse_data.setter
    def parse_data(self, TOKEN ):
        self.__parse_data = {
            "url":f"https://webservice.hobolink.com/ws/data/file/{self.__format}/user/{self.__user_id}?loggers={self.__logger}&start_date_time={self.start_time}&end_date_time={self.end_time}",
            "body":{
                "loggers":[self.__logger],
                "start_date_time":self.start_time
            },
            "headers":{
                'Accept':'application/json',
                "authorization":f"Bearer {TOKEN}"
            }
        }

    @property
    def data(self):
        return self.__data

    def __postData(self):
        url_token = self.__parse_token
        response = requests.post(url=url_token['url'],data=url_token['body'],headers=url_token['headers'])
        TOKEN = response.json()
        self.parse_data = TOKEN['access_token']
        self.__data = requests.get(url=self.parse_data['url'],headers=self.parse_data['headers']).json()

    # Name of each sensor measurement type
    @property
    def sensorsNames(self) -> list:
        observation_list = self.__data['observation_list']
        self.memory = []
        for e in observation_list:
            if e['sensor_measurement_type'] not in self.memory:
                self.memory.append(e['sensor_measurement_type'])
        return self.memory

    def splitBySensorName(self, sensorName):
        return list(filter(lambda x : x['sensor_measurement_type'] == sensorName,self.__data['observation_list']))
    
    def splitTimeValues(self, data):
        time = [e['timestamp'].split(" ")[1][:5] for e in data]
        values_si = [e['si_value'] for e in data]
        values_us = [e['us_value'] for e in data]
        return (time, values_si, values_us)

    # TODO: No toda la data de los sensores tiene la misma longitud
    @property
    def dataSensors(self) -> object:
        sensors = self.sensorsNames
        sensors.remove("Battery")
        obj = {}
        for e in sensors:
            stn = self.splitBySensorName(e)
            time, values_si, values_us = self.splitTimeValues(stn)
            obj[e] = {"si":values_si, "us":values_us}
        return obj
    
    @property
    def timeStation(self):
        sensors = self.sensorsNames
        stn = self.splitBySensorName(sensors[0])
        time, values_si, values_us = self.splitTimeValues(stn)
        return time