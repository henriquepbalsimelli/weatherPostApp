from dataclasses import dataclass, field
import decimal


@dataclass
class CityWeatherDataDto:
    name: str = field(default_factory=str)
    lon: decimal = field(default_factory=decimal)
    lat: decimal = field(default_factory=decimal)
    country: str = field(default_factory=str)
