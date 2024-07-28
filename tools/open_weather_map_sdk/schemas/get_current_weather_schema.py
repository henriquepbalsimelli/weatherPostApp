

from marshmallow import EXCLUDE, Schema, fields, post_load

from tools.open_weather_map_sdk.dtos.current_weather_response_dto import WeatherDayResponseDto, MainDataDto, WeatherDataDto


class MainData(Schema):
    temp = fields.Decimal(
        allow_none=False,
        required=True
    )
    @post_load
    def create_dto(self, data, **kwargs) -> MainDataDto:
        return MainDataDto(**data)

class WeatherData(Schema):
    description = fields.String(
        allow_none=False,
        required=True
    )
    @post_load
    def create_dto(self, data, **kwargs) -> WeatherDataDto:
        return WeatherDataDto(**data)


class WeatherDaySchema(Schema):
    main = fields.Nested(
        MainData(unknown=EXCLUDE),
        allow_none=False,
        required=True
    )
    weather = fields.List(
        fields.Nested(WeatherData(unknown=EXCLUDE)),
        allow_none=False,
        required=True
    )
    dt = fields.Integer(
        required=True,
        allow_none=False
    )

    @post_load
    def make_object(self, data, **kwargs) -> WeatherDayResponseDto:
        return WeatherDayResponseDto(**data)