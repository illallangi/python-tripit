from typing import ClassVar

import diffsync

from illallangi.tripit import TripItClient
from illallangi.tripit.diffsyncmodels import Flight


class AirTransportAdapter(diffsync.Adapter):
    Flight = Flight

    top_level: ClassVar = [
        "Flight",
    ]

    type = "tripit_tripit"

    def load(
        self,
    ) -> None:
        for obj in TripItClient().get_flights():
            if (
                not obj["Arrival"]
                or not obj["ArrivalTimeZone"]
                or not obj["Departure"]
                or not obj["DepartureTimeZone"]
                or not obj["Destination"]
                or not obj["Origin"]
            ):
                continue
            self.add(
                Flight(
                    arrival=obj["Arrival"],
                    arrival_timezone=obj["ArrivalTimeZone"],
                    departure=obj["Departure"],
                    departure_timezone=obj["DepartureTimeZone"],
                    destination=obj["Destination"],
                    origin=obj["Origin"],
                ),
            )
