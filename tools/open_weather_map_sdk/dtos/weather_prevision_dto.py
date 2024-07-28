

from dataclasses import dataclass, field
from typing import List

from tools.open_weather_map_sdk.dtos.current_weather_response_dto import WeatherDayResponseDto

@dataclass
class CityDto:
    timezone: int = field(default_factory=int)

@dataclass
class WeatherPrevisionDto:
    list: List[WeatherDayResponseDto] = field(default_factory=List[WeatherDayResponseDto])
    city: CityDto = field(default_factory=CityDto)