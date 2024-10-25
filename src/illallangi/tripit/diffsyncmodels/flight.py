from datetime import date, datetime

import diffsync


class Flight(
    diffsync.DiffSyncModel,
):
    _modelname = "Flight"
    _identifiers = (
        "departure",
        "flight_number",
    )
    _attributes = (
        "airline__iata",
        "arrival_timezone",
        "arrival",
        "departure_timezone",
        "destination__iata",
        "destination_city",
        "destination_gate",
        "destination_terminal",
        "flight_class",
        "origin__iata",
        "origin_city",
        "origin_gate",
        "origin_terminal",
        "passenger",
        "seat",
        "sequence_number",
        "trip__name",
        "trip__start",
    )

    departure: datetime
    flight_number: str

    airline__iata: str
    arrival_timezone: str
    arrival: datetime
    departure_timezone: str
    destination__iata: str
    destination_city: str
    destination_gate: str | None
    destination_terminal: str | None
    flight_class: str | None
    origin__iata: str
    origin_city: str
    origin_gate: str | None
    origin_terminal: str | None
    passenger: str | None
    seat: str | None
    sequence_number: str
    trip__name: str
    trip__start: date

    @classmethod
    def create(
        cls,
        adapter: diffsync.Adapter,
        ids: dict,
        attrs: dict,
    ) -> "Flight":
        raise NotImplementedError

    def update(
        self,
        attrs: dict,
    ) -> "Flight":
        raise NotImplementedError

    def delete(
        self,
    ) -> "Flight":
        raise NotImplementedError
