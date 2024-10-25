from collections.abc import Generator
from datetime import date
from typing import Any

from more_itertools import first
from openlocationcode import openlocationcode as olc

from illallangi.tripit.models import Trip


def get_start(
    trip: dict[str, Any],
) -> str:
    return date.fromisoformat(
        trip["start_date"],
    )


def get_end(
    trip: dict[str, Any],
) -> str:
    return date.fromisoformat(
        trip["end_date"],
    )


def get_name(
    trip: dict[str, Any],
) -> str:
    return trip["display_name"]


def get_open_location_code(
    trip: dict[str, Any],
) -> str:
    return olc.encode(
        float(trip["PrimaryLocationAddress"]["latitude"]),
        float(trip["PrimaryLocationAddress"]["longitude"]),
    )


class TripMixin:
    _trips = None

    def get_trips(
        self,
        *_: list[Any],
        debug: bool = False,
        progress: bool = True,
        trip_id: int | None = None,
    ) -> Generator[Trip, Any, None]:
        if not self._trips:
            self._trips = list(
                self.get_objects(
                    "Trip",
                    self.base_url
                    / "list"
                    / "trip"
                    / "traveler"
                    / "true"
                    / "past"
                    / "true"
                    / "include_objects"
                    / "false",
                    self.base_url
                    / "list"
                    / "trip"
                    / "traveler"
                    / "true"
                    / "past"
                    / "false"
                    / "include_objects"
                    / "false",
                    progress=progress,
                )
            )

        # trip_id=int(trip["id"]),
        for trip in self._trips:
            if not trip_id or trip_id == int(trip["id"]):
                yield Trip(
                    start=get_start(trip),
                    name=get_name(trip),
                    end=get_end(trip),
                    open_location_code=get_open_location_code(trip),
                    **(
                        {
                            "api": trip["@api"],
                            "trip": {
                                k: v for k, v in trip.items() if k not in ["@api"]
                            },
                        }
                        if debug
                        else {}
                    ),
                )

    def get_trip(
        self,
        trip_id: int,
    ) -> Trip:
        return first(
            self.get_trips(
                progress=False,
                trip_id=trip_id,
            ),
            None,
        )
