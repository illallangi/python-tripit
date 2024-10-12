from collections.abc import Generator
from datetime import datetime, timezone
from typing import Any

import more_itertools

from illallangi.tripit.utils import try_jsonpatch


class FlightMixin:
    def get_flights(
        self,
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
                yield {
                    "Origin": segment.get("start_airport_code"),
                    "Destination": segment.get("end_airport_code"),
                    "Departure": datetime.fromisoformat(
                        f'{segment["StartDateTime"]["date"]}T{segment["StartDateTime"]["time"]}{segment["StartDateTime"]["utc_offset"]}',
                    ).astimezone(timezone.utc),
                    "DepartureTimeZone": segment["StartDateTime"]["timezone"],
                    "Arrival": datetime.fromisoformat(
                        f'{segment["EndDateTime"]["date"]}T{segment["EndDateTime"]["time"]}{segment["EndDateTime"]["utc_offset"]}',
                    ).astimezone(timezone.utc),
                    "ArrivalTimeZone": segment["EndDateTime"]["timezone"],
                    "@air": {k: v for k, v in air.items() if k not in ["@api", "Segment"]},
                    "@api": air["@api"],
                    "@segment": segment,
                }
