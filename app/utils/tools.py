

import datetime


def get_date_from_timestamp_and_tzint(
        timestamp: str,
        tz_int: int
) -> datetime.datetime:
    tzinfo = datetime.timezone(datetime.timedelta(seconds=tz_int)) 

    date = datetime.datetime.fromtimestamp(timestamp, tz=tzinfo)

    return date