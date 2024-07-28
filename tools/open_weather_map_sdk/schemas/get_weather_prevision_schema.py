

from marshmallow import EXCLUDE, Schema, fields, post_load

from tools.open_weather_map_sdk.dtos.weather_prevision_dto import CityDto, WeatherPrevisionDto

from tools.open_weather_map_sdk.schemas.get_current_weather_schema import WeatherDaySchema

class CitySchema(Schema):
    timezone: int = fields.Integer(
        required=True,
        allow_none=False
    )

    @post_load
    def make_object(self, data, **kwargs) -> CityDto:
        return CityDto(**data)
    
class WeatherPrevisionSchema(Schema):
    list = fields.List(
        fields.Nested(WeatherDaySchema(unknown=EXCLUDE)),
        allow_none=False,
        required=True
    )

    city = fields.Nested(
        CitySchema(unknown=EXCLUDE),
        required=True,
        allow_none=False
    )


    @post_load
    def make_object(self, data, **kwargs) -> WeatherPrevisionDto:
        return WeatherPrevisionDto(**data)