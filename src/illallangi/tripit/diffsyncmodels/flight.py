from datetime import datetime

import diffsync


class Flight(diffsync.DiffSyncModel):
    _modelname = "Flight"
    _identifiers = (
        "departure",
        "origin",
    )
    _attributes = (
        "arrival_timezone",
        "arrival",
        "departure_timezone",
        "destination",
    )

    arrival_timezone: str
    arrival: datetime
    departure_timezone: str
    departure: datetime
    destination: str
    origin: str

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
