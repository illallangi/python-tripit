from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from attrs import define, field, validators

from illallangi.tripit.models.airline import AirlineKey
from illallangi.tripit.models.airport import AirportKey
from illallangi.tripit.models.trip import TripKey


@define(kw_only=True)
class FlightKey:
    # Natural Keys

    departure: datetime = field(
        validator=[
            validators.instance_of(datetime),
        ],
    )

    flight_number: str = field(
        validator=[
            validators.instance_of(str),
            validators.matches_re(r"^[0-9A-Z]{2}[ 0-9]{4}$"),
        ],
    )


@define(kw_only=True)
class Flight(FlightKey):
    # Fields

    airline: AirlineKey = field(
        validator=[
            validators.instance_of(AirlineKey),
        ],
    )
    arrival_timezone: ZoneInfo = field(
        validator=[
            validators.instance_of(ZoneInfo),
        ],
    )
    arrival: datetime = field(
        validator=[
            validators.instance_of(datetime),
        ],
    )
    departure_timezone: ZoneInfo = field(
        validator=[
            validators.instance_of(ZoneInfo),
        ],
    )
    destination_city: str = field(
        validator=[
            validators.instance_of(str),
        ],
    )
    destination_gate: str | None = field(
        validator=[
            validators.instance_of(str | None),
        ],
    )
    destination_terminal: str | None = field(
        validator=[
            validators.instance_of(str | None),
        ],
    )
    destination: AirportKey = field(
        validator=[
            validators.instance_of(AirportKey),
        ],
    )
    flight_class: str | None = field(
        validator=[
            validators.instance_of(str | None),
        ],
    )
    origin_city: str = field(
        validator=[
            validators.instance_of(str),
        ],
    )
    origin_gate: str | None = field(
        validator=[
            validators.instance_of(str | None),
        ],
    )
    origin_terminal: str | None = field(
        validator=[
            validators.instance_of(str | None),
        ],
    )
    origin: AirportKey = field(
        validator=[
            validators.instance_of(AirportKey),
        ],
    )
    passenger: str | None = field(
        validator=[
            validators.instance_of(str | None),
        ],
    )
    seat: str | None = field(
        validator=[
            validators.instance_of(str | None),
            # validators.matches_re(r"^[0-9]{2}[A-Z]$"),
        ],
    )
    sequence_number: str = field(
        validator=[
            validators.instance_of(str),
        ],
    )
    trip: TripKey | None = field(
        validator=[
            validators.instance_of(TripKey | None),
        ],
    )

    # API Responses

    _air: dict[str, Any] | None = field(
        default=None,
        validator=[
            validators.instance_of(dict | None),
        ],
    )
    _api: dict[str, Any] | None = field(
        default=None,
        validator=[
            validators.instance_of(dict | None),
        ],
    )
    _segment: dict[str, Any] | None = field(
        default=None,
        validator=[
            validators.instance_of(dict | None),
        ],
    )
