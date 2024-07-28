import decimal
import logging
from typing import List
from fastapi import HTTPException
from marshmallow import EXCLUDE, ValidationError
import requests
from configurations import get_env
from tools.open_weather_map_sdk.dtos.current_weather_response_dto import WeatherDayResponseDto
from tools.open_weather_map_sdk.dtos.weather_prevision_dto import WeatherPrevisionDto
from tools.open_weather_map_sdk.schemas.get_current_weather_schema import WeatherDaySchema
from tools.open_weather_map_sdk.schemas.get_weather_prevision_schema import WeatherPrevisionSchema

class OpenWeatherMapSdk:
    def __init__(self):
        self.__logger = logging.getLogger(__name__)
        self.__weather_app_api_key = get_env('WEATHER_APP_API_KEY')

    def __validate_response(self, response: requests.Response):
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail='Network error' + response.text
            )

    def get_current_weather(
            self,
            lon: decimal,
            lat: decimal
    )-> WeatherDayResponseDto:
        try:
            url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={self.__weather_app_api_key}&lang=pt_br&units=metric'
            
            response = requests.get(
                url=url
            )
            self.__validate_response(response)
            
            return WeatherDaySchema(unknown=EXCLUDE).load(response.json())
        
        except TypeError as e:
            self.__logger.error(msg="INTEGRATION WEATHER MAP ERROR - GET CURRENT WEATHER")
            raise HTTPException(
                status_code=400,
                detail="Houve um problema na identificação das propriedades retornadas pelo serviço terceiro" + str(e.args)
            )
        except ValidationError as e:
            raise HTTPException(
                status_code=400,
                detail="INTEGRATION ERROR - Erro no corpo da resposta"
            )
        except Exception as e:
            self.__logger.error(msg="INTEGRATION WEATHER MAP ERROR - GET CURRENT WEATHER")
            raise e
    
    def get_weather_prevision(
        self,
        lon: decimal,
        lat: decimal
    ) -> WeatherPrevisionDto:
        try:
            url = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={self.__weather_app_api_key}&lang=pt_br&units=metric'
            
            response = requests.get(
                url=url
            )
            self.__validate_response(response)
            json_response = response.json()
            return WeatherPrevisionSchema(unknown=EXCLUDE).load(response.json())
        except TypeError as e:
            self.__logger.error(msg="INTEGRATION WEATHER MAP ERROR - GET WEATHER PREVISION")
            raise HTTPException(
                status_code=400,
                detail="Houve um problema na identificação das propriedades retornadas pelo serviço terceiro" + str(e.args)
            )
        except ValidationError as e:
            raise HTTPException(
                status_code=400,
                detail="INTEGRATION ERROR - Erro no corpo da resposta"
            )
        except Exception as e:
            self.__logger.error(msg="INTEGRATION WEATHER MAP ERROR - GET WEATHER PREVISION")
            raise e