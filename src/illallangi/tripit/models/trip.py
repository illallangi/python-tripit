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
