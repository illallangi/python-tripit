from collections.abc import Generator
from datetime import datetime, timezone
from typing import Any
from zoneinfo import ZoneInfo

import more_itertools

from illallangi.tripit.models import AirlineKey, AirportKey, Flight
from illallangi.tripit.utils import try_jsonpatch

UNKNOWN = None
BUSINESS_CLASS = "Business"
FIRST_CLASS = "First"
PREMIUM_ECONOMY = "Premium Economy"
ECONOMY = "Economy"

CLASSES = {
    "business saver": BUSINESS_CLASS,
    "business": BUSINESS_CLASS,
    "c": UNKNOWN,
    "discount business": BUSINESS_CLASS,
    "e": ECONOMY,
    "economy - e": ECONOMY,
    "economy - h": ECONOMY,
    "economy - k": ECONOMY,
    "economy - m": ECONOMY,
    "economy - n": ECONOMY,
    "economy - q": ECONOMY,
    "economy - s": ECONOMY,
    "economy - y": ECONOMY,
    "economy / k": ECONOMY,
    "economy": ECONOMY,
    "elevate": UNKNOWN,
    "f": FIRST_CLASS,
    "first": FIRST_CLASS,
    "flex y/b (y)": ECONOMY,
    "flex y/b": ECONOMY,
    "flex": UNKNOWN,
    "freedom": UNKNOWN,
    "h": ECONOMY,
    "i": UNKNOWN,
    "k": ECONOMY,
    "l": UNKNOWN,
    "m": ECONOMY,
    "n": ECONOMY,
    "premium economy": PREMIUM_ECONOMY,
    "q": ECONOMY,
    "red e-deal (q)": ECONOMY,
    "red e-deal": ECONOMY,
    "s": ECONOMY,
    "sale": UNKNOWN,
    "saver": UNKNOWN,
    "v": UNKNOWN,
    "y": ECONOMY,
}

TERMINALS = {
    "1": "Terminal 1",
    "2": "Terminal 2",
    "3": "Terminal 3",
    "4": "Terminal 4",
    "5": "Terminal 5",
    "6": "Terminal 6",
    "d": "Terminal D",
    "tbit": "Tom Bradley International",
    "a": "Terminal A",
    "b": "Terminal B",
    "c": "Terminal C",
    "intl": "International",
    "i": "International",
}


def get_departure(
    segment: dict[str, Any],
) -> datetime:
    return datetime.fromisoformat(
        f'{segment["StartDateTime"]["date"]}T{segment["StartDateTime"]["time"]}{segment["StartDateTime"]["utc_offset"]}',
    ).astimezone(timezone.utc)


def get_flight_number(
    segment: dict[str, Any],
) -> str:
    return f'{segment["marketing_airline_code"]}{segment["marketing_flight_number"].rjust(4, " ")}'


def get_airline(
    segment: dict[str, Any],
) -> str:
    return AirlineKey(
        iata=segment["marketing_airline_code"],
    )


def get_arrival_timezone(
    segment: dict[str, Any],
) -> ZoneInfo:
    return ZoneInfo(segment["EndDateTime"]["timezone"])


def get_arrival(
    segment: dict[str, Any],
    tz: timezone = timezone.utc,
) -> datetime:
    return datetime.fromisoformat(
        f'{segment["EndDateTime"]["date"]}T{segment["EndDateTime"]["time"]}{segment["EndDateTime"]["utc_offset"]}',
    ).astimezone(
        tz,
    )


def get_departure_timezone(
    segment: dict[str, Any],
) -> ZoneInfo:
    return ZoneInfo(segment["StartDateTime"]["timezone"])


def get_destination_city(
    segment: dict[str, Any],
) -> str:
    return segment["end_city_name"]


def get_destination_gate(
    segment: dict[str, Any],
) -> str:
    return segment.get("end_gate")


def get_destination_terminal(
    segment: dict[str, Any],
) -> str:
    return (
        TERMINALS[segment["end_terminal"].lower()]
        if "end_terminal" in segment
        else None
    )


def get_destination(
    segment: dict[str, Any],
) -> str:
    return AirportKey(
        iata=segment["end_airport_code"],
    )


def get_flight_class(
    segment: dict[str, Any],
) -> str:
    return (
        CLASSES[segment["service_class"].lower()]
        if "service_class" in segment
        else None
    )


def get_origin_city(
    segment: dict[str, Any],
) -> str:
    return segment["start_city_name"]


def get_origin_gate(
    segment: dict[str, Any],
) -> str:
    return segment.get("start_gate")


def get_origin_terminal(
    segment: dict[str, Any],
) -> str:
    return (
        TERMINALS[segment["start_terminal"].lower()]
        if "start_terminal" in segment
        else None
    )


def get_origin(
    segment: dict[str, Any],
) -> str:
    return AirportKey(
        iata=segment.get("start_airport_code"),
    )


def get_passenger(
    air: dict[str, Any],
) -> str:
    result = ", ".join(
        [
            name
            for name in [
                more_itertools.first(
                    more_itertools.always_iterable(
                        air.get("Traveler", [{}]), base_type=dict
                    )
                ).get("last_name"),
                " ".join(
                    [
                        name
                        for name in [
                            more_itertools.first(
                                more_itertools.always_iterable(
                                    air.get("Traveler", [{}]),
                                    base_type=dict,
                                )
                            ).get("first_name"),
                            more_itertools.first(
                                more_itertools.always_iterable(
                                    air.get("Traveler", [{}]),
                                    base_type=dict,
                                )
                            ).get("middle_name"),
                        ]
                        if name
                    ],
                ),
            ]
            if name
        ]
    )
    return result if result else None


def get_seat(
    segment: dict[str, Any],
) -> str:
    return segment["seats"].lstrip("0") if "seats" in segment else None


def get_sequence_number(
    segment: dict[str, Any],
) -> str:
    return segment["id"][-3:]


class FlightMixin:
    def get_flights(
        self,
        *_: list[Any],
        debug: bool = False,
        progress: bool = True,
    ) -> Generator[dict[str, Any], None, None]:
        for air in self.get_objects(
            "AirObject",
            self.base_url
            / "list"
            / "object"
            / "traveler"
            / "true"
            / "past"
            / "true"
            / "include_objects"
            / "false"
            / "type"
            / "air",
            self.base_url
            / "list"
            / "object"
            / "traveler"
            / "true"
            / "past"
            / "false"
            / "include_objects"
            / "false"
            / "type"
            / "air",
            progress=progress,
        ):
            for segment in [
                try_jsonpatch(
                    segment,
                    segment.get("notes"),
                )
                for segment in more_itertools.always_iterable(
                    air.get("Segment", []),
                    base_type=dict,
                )
            ]:
                # trip_id=int(air["trip_id"]),
                # air_id=int(air["id"]),
                # segment_id=int(segment["id"]),
                yield Flight(
                    departure=get_departure(segment),
                    flight_number=get_flight_number(segment),
                    airline=get_airline(segment),
                    arrival_timezone=get_arrival_timezone(segment),
                    arrival=get_arrival(segment),
                    departure_timezone=get_departure_timezone(segment),
                    destination_city=get_destination_city(segment),
                    destination_gate=get_destination_gate(segment),
                    destination_terminal=get_destination_terminal(segment),
                    destination=get_destination(segment),
                    flight_class=get_flight_class(segment),
                    origin_city=get_origin_city(segment),
                    origin_gate=get_origin_gate(segment),
                    origin_terminal=get_origin_terminal(segment),
                    origin=get_origin(segment),
                    passenger=get_passenger(air),
                    seat=get_seat(segment),
                    sequence_number=get_sequence_number(segment),
                    trip=self.get_trip(
                        int(air["trip_id"]),
                    ),
                    **(
                        {
                            "air": {
                                k: v
                                for k, v in air.items()
                                if k not in ["@api", "Segment"]
                            },
                            "api": air["@api"],
                            "segment": segment,
                        }
                        if debug
                        else {}
                    ),
                )
