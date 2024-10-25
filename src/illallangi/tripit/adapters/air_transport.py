from typing import ClassVar

import diffsync
from cattrs import global_converter, structure, unstructure

from illallangi.tripit import TripItClient
from illallangi.tripit.diffsyncmodels import Flight, Trip


@global_converter.register_structure_hook
def trip_structure_hook(
    value: dict,
    type: type,  # noqa: A002, ARG001
) -> Trip:
    return Trip(
        **value,
    )


@global_converter.register_structure_hook
def flight_structure_hook(
    value: dict,
    type: type,  # noqa: A002, ARG001
) -> Flight:
    return Flight(
        airline__iata=str(value.pop("airline")["iata"]),
        arrival_timezone=str(value.pop("arrival_timezone")),
        departure_timezone=str(value.pop("departure_timezone")),
        destination__iata=str(value.pop("destination")["iata"]),
        origin__iata=str(value.pop("origin")["iata"]),
        trip__name=value["trip"]["name"],
        trip__start=value.pop("trip")["start"],
        **value,
    )


class AirTransportAdapter(diffsync.Adapter):
    def __init__(
        self,
        *args: list,
        **kwargs: dict,
    ) -> None:
        super().__init__()
        self.client = TripItClient(
            *args,
            **kwargs,
        )

    Flight = Flight
    Trip = Trip

    top_level: ClassVar = [
        "Flight",
        "Trip",
    ]

    type = "tripit_air_transport"

    def load(
        self,
        *args: list,
        **kwargs: dict,
    ) -> None:
        for obj in self.client.get_trips(
            *args,
            **kwargs,
        ):
            d = unstructure(
                obj,
            )
            o = structure(
                d,
                Trip,
            )
            self.add(
                o,
            )

        for obj in self.client.get_flights(
            *args,
            **kwargs,
        ):
            d = unstructure(
                obj,
            )
            o = structure(
                d,
                Flight,
            )
            self.add(
                o,
            )
