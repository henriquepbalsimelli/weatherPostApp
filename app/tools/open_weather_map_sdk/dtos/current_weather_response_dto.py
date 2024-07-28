from datetime import datetime
import decimal

from dataclasses import dataclass, field
from typing import List

@dataclass
class MainDataDto:
    temp: decimal = field(default_factory=decimal)

@dataclass
class WeatherDataDto:
    description: str = field(default_factory=str)

@dataclass
class WeatherDayResponseDto:
    main: MainDataDto = field(default_factory=MainDataDto)
    weather: List[WeatherDataDto] = field(default_factory=List[WeatherDataDto])
    dt: int = field(default_factory=int)


