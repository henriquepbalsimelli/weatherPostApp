

from decimal import Decimal
from typing import Union
from unittest.mock import Mock
from fastapi import HTTPException
from marshmallow import EXCLUDE, ValidationError
import pytest
import requests
from app.services.x_services.x_publication_service import XPublicationService
from app.tools.open_weather_map_sdk.dtos.current_weather_response_dto import MainDataDto, WeatherDataDto, WeatherDayResponseDto
from app.tools.open_weather_map_sdk.dtos.weather_prevision_dto import CityDto, WeatherPrevisionDto
from app.tools.open_weather_map_sdk.requests.sdk import OpenWeatherMapSdk
import datetime

from app.tools.open_weather_map_sdk.schemas.get_current_weather_schema import WeatherDaySchema
from app.tools.open_weather_map_sdk.schemas.get_weather_prevision_schema import WeatherPrevisionSchema
from app.tools.x_tools.sdk import XSdk


def test_city_does_not_exist():
    x_publication_service = XPublicationService()
    with pytest.raises(HTTPException) as excinfo:
        x_publication_service.handle_create_x_publication(city_name='NAME')

    assert excinfo.value.detail == "City not found"

def test_created_post_ok():
    weather_sdk_mock = OpenWeatherMapSdk()

    now = datetime.datetime.timestamp(datetime.datetime.now())
    tomorrow = datetime.datetime.timestamp(datetime.datetime.now() + datetime.timedelta(days=1))
    two_days_plus = datetime.datetime.timestamp(datetime.datetime.now() + datetime.timedelta(days=2))
    three_days_plus = datetime.datetime.timestamp(datetime.datetime.now() + datetime.timedelta(days=3))
    four_days_plus = datetime.datetime.timestamp(datetime.datetime.now() + datetime.timedelta(days=4))
    five_days_plus = datetime.datetime.timestamp(datetime.datetime.now() + datetime.timedelta(days=5))

    
    weather_sdk_mock.get_current_weather = Mock(spec=weather_sdk_mock.get_current_weather, wraps=weather_sdk_mock.get_current_weather)
    weather_sdk_mock.get_current_weather.return_value = WeatherDayResponseDto(
        main=MainDataDto(
            temp=1
        ),
        weather=[WeatherDataDto(
            description='nublado'
        )],
        dt=now
    )

    weather_sdk_mock.get_weather_prevision = Mock(sped=weather_sdk_mock.get_weather_prevision, wraps= weather_sdk_mock.get_weather_prevision)
    weather_sdk_mock.get_weather_prevision.return_value = WeatherPrevisionDto(
        city=CityDto(
                timezone=-10800
            ),
        list = [
            WeatherDayResponseDto(
                main=MainDataDto(temp=1),
                weather=WeatherDataDto(description='nublado'),
                dt=tomorrow
                ),
            WeatherDayResponseDto(
                main=MainDataDto(temp=1),
                weather=WeatherDataDto(description='nublado'),
                dt=two_days_plus
                ),
            WeatherDayResponseDto(
                main=MainDataDto(temp=1),
                weather=WeatherDataDto(description='nublado'),
                dt=three_days_plus
                ),
            WeatherDayResponseDto(
                main=MainDataDto(temp=1),
                weather=WeatherDataDto(description='nublado'),
                dt=four_days_plus
                ),
            WeatherDayResponseDto(
                main=MainDataDto(temp=1),
                weather=WeatherDataDto(description='nublado'),
                dt=five_days_plus
                ),
            ],
    )

    x_sdk = XSdk()

    x_sdk.create_post = Mock(sped=x_sdk.create_post, wraps=x_sdk.create_post)
    x_sdk.create_post.return_value = requests.Response
    
    x_publication_service = XPublicationService(
        weather_sdk=weather_sdk_mock,
        x_sdk=x_sdk
    )

    x_publication_service.handle_create_x_publication(city_name='Brasilia')
    weather_sdk_mock.get_current_weather.assert_called_once()
    weather_sdk_mock.get_weather_prevision.assert_called_once()
    x_sdk.create_post.assert_called_once()


def testing_integration_weather_day_schema_ok():
    json = {
        "main": {
            "temp": 1
        },
        "weather": [{
            "description": "str"
        }],
        "dt": 1,
        "ignored_property": "str"
    }

    dto: WeatherDayResponseDto = WeatherDaySchema(unknown=EXCLUDE).load(json)
    assert dto.main.temp == json.get('main').get("temp")
    assert dto.weather[0].description == json.get('weather')[0].get("description")
    assert dto.dt == json.get('dt')


@pytest.mark.parametrize(
        'temp, description, dt', 
        [
            (1.0, 1, 1),
            ("str", "str", 1),
            (1.0, "str", "str"),
        ])
def testing_weather_day_schema_invalid_data_types(temp: Union[str, Decimal], description: Union[str, int], dt: Union[str, int]):
    json = {
        "main": {
            "temp": temp
        },
        "weather": [{
            "description": description
        }],
        "dt": dt
    }

    with pytest.raises(ValidationError) as excinfo:
        WeatherDaySchema(unknown=EXCLUDE).load(json)

    if isinstance(description, int):
        assert excinfo.value.messages.get('weather')[0].get('description') == ['Not a valid string.']

    if isinstance(temp, str):
        assert excinfo.value.messages.get('main').get('temp') == ['Not a valid number.']

    if isinstance(dt, str):
        assert excinfo.value.messages.get('dt') == ['Not a valid integer.']


def testing_weather_prevision_schema_ok():
    json = {
        'list': [
                {
                    'dt': 1722178800, 
                    'main': {'temp': 22.7}, 
                    'weather': [
                        {
                            "description": "str"
                        }
                    ]
                }
            ], 
        'city': {
            'timezone': -10800, 
        }
    }
    
    dto: WeatherPrevisionDto = WeatherPrevisionSchema().load(json)
    assert dto.list[0].dt == json.get("list")[0].get('dt')
    assert dto.list[0].main.temp == Decimal(str(json.get("list")[0].get('main').get("temp")))
    assert dto.list[0].weather[0].description == json.get("list")[0].get('weather')[0].get("description")
    assert dto.city.timezone == json.get("city").get('timezone')

@pytest.mark.parametrize(
        'temp, description, dt, tz', 
        [
            (1.0, 1, 1, 1),
            ("str", "str", 1, 1),
            (1.0, "str", "str", 1),
            (1.0, "str", 1, "str"),
        ])
def testing_weather_prevision_schema_invalid_data_types(
    temp: Union[str, Decimal], 
    description: Union[str, int], 
    dt: Union[str, int],
    tz: Union[str, int]
    ):
    json = {
        'list': [
                {
                    'dt': dt, 
                    'main': {'temp': temp}, 
                    'weather': [
                        {
                            "description": description
                        }
                    ]
                }
            ], 
        'city': {
            'timezone': tz, 
        }
    }
    with pytest.raises(ValidationError) as excinfo:
        dto: WeatherPrevisionDto = WeatherPrevisionSchema().load(json)

    if isinstance(description, int):
        assert excinfo.value.messages.get('list')[0].get('weather')[0].get('description') == ['Not a valid string.']

    if isinstance(temp, str):
        assert excinfo.value.messages.get('list')[0].get('main').get('temp') == ['Not a valid number.']

    if isinstance(dt, str):
        assert excinfo.value.messages.get('list')[0].get('dt') == ['Not a valid integer.']

    if isinstance(tz, str):
        assert excinfo.value.messages.get('city').get('timezone') == ['Not a valid integer.']