import more_itertools


class FlightMixin:
    def get_flights(
        self,
    ):
        yield from [
            {
                **segment,
                "@air": {k: v for k, v in air.items() if k not in ["@api", "Segment"]},
                "@api": air["@api"],
            }
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
            )
            for segment in more_itertools.always_iterable(
                air.get("Segment", []),
                base_type=dict,
            )
        ]
