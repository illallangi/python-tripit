from typing import ClassVar

import diffsync

from illallangi.tripit import TripItClient
from illallangi.tripit.diffsyncmodels import Flight, Trip


class AirTransportAdapter(diffsync.Adapter):
    Flight = Flight
    Trip = Trip

    top_level: ClassVar = [
        "Flight",
        "Trip",
    ]

    type = "tripit_tripit"

    def load(
        self,
    ) -> None:
        for obj in TripItClient().get_flights():
            self.add(
                Flight(
                    airline=obj["Airline"],
                    arrival=obj["Arrival"],
                    arrival_timezone=obj["ArrivalTimeZone"],
                    departure=obj["Departure"],
                    departure_timezone=obj["DepartureTimeZone"],
                    destination=obj["Destination"],
                    destination_city=obj["DestinationCity"],
                    destination_terminal=obj["DestinationTerminal"],
                    flight_class=obj["FlightClass"],
                    flight_number=obj["FlightNumber"],
                    origin=obj["Origin"],
                    origin_city=obj["OriginCity"],
                    origin_terminal=obj["OriginTerminal"],
                ),
            )
        for obj in self.client.get_trips():
            self.add(
                Trip(
                    end=obj["End"],
                    name=obj["Name"],
                    start=obj["Start"],
                ),
            )
