class TripMixin:
    def get_trips(
        self,
    ):
        yield from [
            {
                "ID": trip["id"],
                "Name": trip["display_name"],
                "@api": trip["@api"],
                "@trip": {k: v for k, v in trip.items() if k not in ["@api"]},
            }
            for trip in self.get_objects(
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
            )
        ]