import logging
from operator import indexOf
from typing import List

from fastapi import HTTPException
from app.dtos.city_data_dto import CityWeatherDataDto
from app.utils.tools import get_date_from_timestamp_and_tzint
from tools.open_weather_map_sdk.dtos.current_weather_response_dto import WeatherDayResponseDto
from tools.open_weather_map_sdk.dtos.weather_prevision_dto import WeatherPrevisionDto
from tools.open_weather_map_sdk.requests.sdk import OpenWeatherMapSdk
import pandas as pd

class XPublicationService():
    def __init__(
            self,
            weather_sdk = OpenWeatherMapSdk()
        ):
        self.__logger = logging.getLogger(__name__)
        self.__weather_sdk = weather_sdk

    def handle_create_x_publication(self, city_name: str):
        try:
            city_data = self.__get_city_data()
            
            city = next(filter(lambda city: city.name == city_name, city_data), None)
            
            if not city:
                self.__logger.error(msg="ERROR DURING CITY IDENTIFICATION")
                raise HTTPException(status_code=404, detail="City not found")
            
            current_weather = self.__weather_sdk.get_current_weather(
                lon=city.lon,
                lat=city.lat
            )

            weather_prevision = self.__weather_sdk.get_weather_prevision(
                lon=city.lon,
                lat=city.lat
            )

            self.format_date(weather_prevision=weather_prevision, current_weather=current_weather)

            average_temp_by_date = self.__get_temp_by_dates(
                weather_prevision=weather_prevision
            )

            post_string = self.__create_weather_publication_str(
                average_temp_by_date=average_temp_by_date,
                current_temp=current_weather,
                city_name=city_name
            )

            return post_string
        except Exception as e:
            raise e
    
    def __get_city_data(self) -> List[CityWeatherDataDto]:
        cities_file = pd.read_excel(
            'cities_list.xlsx'
        )

        cities_formated_list = []
        for row in cities_file.values:
            cities_formated_list.append(
                CityWeatherDataDto(
                    name=row[0],
                    lon=row[1],
                    lat=row[2],
                    country=row[3]
                )
            )
        return cities_formated_list
    
    def format_date(self, weather_prevision: WeatherPrevisionDto, current_weather: WeatherDayResponseDto):
        current_weather.dt = get_date_from_timestamp_and_tzint(
            timestamp=current_weather.dt,
            tz_int=weather_prevision.city.timezone
        ).strftime("%d/%m")
        for item in weather_prevision.list:
            item.dt = get_date_from_timestamp_and_tzint(
                timestamp=item.dt,
                tz_int=weather_prevision.city.timezone
            ).strftime("%d/%m")
    
    def __get_temp_by_dates(self, weather_prevision: WeatherPrevisionDto):
        prevision_by_dates = {}
        
        for prevision in weather_prevision.list:
            
            data_exists = prevision_by_dates.get(prevision.dt, None)

            if data_exists:
                continue
            
            date_temperatures = [temp.main.temp for temp in weather_prevision.list if temp.dt == prevision.dt]

            prevision_by_dates[prevision.dt] = {
                'temperatures': date_temperatures,
                'average': round(sum(date_temperatures)/len(date_temperatures))
            }
                
        return prevision_by_dates
    
    def __create_weather_publication_str(self, average_temp_by_date: dict, current_temp: WeatherDayResponseDto, city_name: str):
        final_str = ''
        index = 0
        for temp_date, temp_data in average_temp_by_date.items():
            length = average_temp_by_date.__len__()
            if index == 0:
                final_str = f"{current_temp.main.temp}°C e {current_temp.weather[0].description} em {city_name} em {current_temp.dt}. Média para os próximos dias: "
                index += 1
                continue

            if index == length - 1:
                final_str = final_str + f"e {temp_data.get('average')}°C em {temp_date}."
                index += 1
                continue

            final_str = final_str + f"{temp_data.get('average')}°C em {temp_date}, "
            index += 1
        return final_str

