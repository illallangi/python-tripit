from datetime import datetime

import diffsync


class Trip(
    diffsync.DiffSyncModel,
):
    _modelname = "Trip"
    _identifiers = (
        "name",
        "start",
    )
    _attributes = (
        "end",
        "open_location_code",
    )

    name: str
    start: datetime

    end: datetime
    open_location_code: str

    @classmethod
    def create(
        cls,
        adapter: diffsync.Adapter,
        ids: dict,
        attrs: dict,
    ) -> "Trip":
        raise NotImplementedError

    def update(
        self,
        attrs: dict,
    ) -> "Trip":
        raise NotImplementedError

    def delete(
        self,
    ) -> "Trip":
        raise NotImplementedError
