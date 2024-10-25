from datetime import date
from typing import Any

from attrs import define, field, validators


@define(kw_only=True)
class TripKey:
    # Natural Keys

    start: date = field(
        validator=[
            validators.instance_of(date),
        ],
    )
    name: str = field(
        validator=[
            validators.instance_of(str),
        ],
    )


@define(kw_only=True)
class Trip(TripKey):
    # Fields

    end: date = field(
        validator=[
            validators.instance_of(date),
        ],
    )

    open_location_code: str = field(
        validator=[
            validators.instance_of(str),
            validators.matches_re(
                r"^[23456789CFGHJMPQRVWX]{8}\+[23456789CFGHJMPQRVWX]{2,}$"
            ),
        ],
    )

    # API Responses

    _api: dict[str, Any] | None = field(
        default=None,
        validator=[
            validators.instance_of(dict | None),
        ],
    )
    _trip: dict[str, Any] | None = field(
        default=None,
        validator=[
            validators.instance_of(dict | None),
        ],
    )
